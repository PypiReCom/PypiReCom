from bs4 import BeautifulSoup
import requests
import csv
import os
import nltk
import pandas as pd
import json
from nltk.corpus import stopwords
import networkx as nx
# nltk.download('stopwords')
import pyTigerGraph as tg
from datetime import date
from time import time
import logging
from backend_config import *
logging.basicConfig(filename='logs.txt', filemode='a', format='%(asctime)s %(levelname)s-%(message)s', datefmt='%d-%m-%y')



def get_packages(link):
    '''
    Input: Link of the endpoint -> link
    
    This link is used to receive the HTML response and BeautifulSoup is used to scrape the data about names of packages from the response.

    Return: List of package received from the HTML response
    '''
    packages = []
    # Creating a BeautifulSoup
    soup = BeautifulSoup(requests.get(link).content,'html.parser')
    # Finding the specific class of object in which we have package name
    html_data = soup.find_all('a',class_="package-snippet")
    # Adding the name of packages to the list
    for package in html_data:
        packages.append(str(package).split('/')[2])
    return packages



def fetch_data(response):
    '''
    Input: Json of package meta data -> response

    This function takes the data in json and add the nesseary things of the data in a list 

    Return: List of data containing package name,author,email,license,development status,programming language and dependency
    '''
    name = response['info']['name'] 
    author = response['info']['author'] if response['info']['author'] != None else ''
    author_email = response['info']['author_email'] if response['info']['author_email'] != None else ''
    license = response['info']['license'] if response['info']['license'] != None else ''
    programming_lang = set()
    development_status = ''
    classifier = response["info"]['classifiers'] if response["info"]['classifiers'] != None else []
    for classifier in response["info"]['classifiers']:
        classifier_list = classifier.split(' :: ')
        if 'Development Status' in classifier_list:
            development_status = classifier_list[-1]
        elif 'Programming Language' in classifier_list:
            programming_lang.add(classifier_list[1])
    package_dependency = set()
    requires_dist = response["info"]['requires_dist'] if response["info"]['requires_dist'] != None else []
    for dependency in requires_dist:
        package_dependency.add(dependency.split()[0])
    
    return [name,author,author_email,license,development_status,programming_lang,package_dependency]



def create_directory(Search_Context):
    '''
    Input: Space seperaetd keywords to be searched -> Search_Context (In address or any operation _ is used to join the Search_Context)

    This function creates the folder in ../library named as {Search_Context}

    Then, creates 3 csv(s) in the folder adding the name of attributes/columns in each csv
    '''
    directory = '_'.join(Search_Context.split())

    # Defining the path as .../library/{directory}
    path = os.path.join(parent_dir, directory)

    # Creating the directory
    try:
        os.mkdir(path)
    except Exception as e:
        print("Folder can not be created.")
        logging.error('Folder can not be created for ' + '_'.join(Search_Context.split()) + 'Exception: ' + str(e))
        return {"Status Code" : Status_Code["Fail"], "Description" : "Folder can not be created"}

    # Creating the differnt csv(s)
    base_directory = parent_dir+'_'.join(Search_Context.split())
    try:
        with open(base_directory+"/Package_Basic_Data.csv","a", newline='') as file:
            csv_file = csv.writer(file)
            csv_file.writerow(['name','author','author_email','license','development_status'])
        with open(base_directory+"/Package_Dependency.csv","a", newline='') as file:
            csv_file = csv.writer(file)
            csv_file.writerow(['name','dependency_pkg'])
        with open(base_directory+"/Package_Prog_Lang.csv","a", newline='') as file:
            csv_file = csv.writer(file)
            csv_file.writerow(['name','language'])
    except:
        print('Error in creating file.')
        logging.error('Error in creating file in ' + '_'.join(Search_Context.split()) + ' folder')
        return {"Status Code" : Status_Code["Fail"], "Description" : "Error in file creation"}
    
    return {"Status Code" : Status_Code["Success"] , "Description" : "Folder & files created", "Path" : base_directory}



def save_data(Search_Context,data):
    '''
    Input: Space seperaetd keywords to be searched -> Search_Context (In address or any operation _ is used to join the Search_Context), 
           List of data containing package name,author,email,license,development status,programming language and dependency -> data
    
    This function loads data in 3 csv(s) in the ../library/{Search_Context} and inserts the nessesary data in each csv.
    '''
    # Inserting Data into Different files
    base_directory = parent_dir+'_'.join(Search_Context.split())
    try:
        # Saving data to files
        name,author,author_email,license,development_status,programming_lang,package_dependency = data
        with open(base_directory+"/Package_Basic_Data.csv","a", newline='') as file:
            csv_file = csv.writer(file)
            csv_file.writerow([name,author,author_email,license,development_status])
        with open(base_directory+"/Package_Dependency.csv","a", newline='') as file:
            csv_file = csv.writer(file)
            for dependency_pkg in package_dependency:
                csv_file.writerow([name,dependency_pkg])
        with open(base_directory+"/Package_Prog_Lang.csv","a", newline='') as file:
            csv_file = csv.writer(file)
            for language in programming_lang:
                csv_file.writerow([name,language])
    except:
        logging.error('Error in saving data for ' + '_'.join(Search_Context.split()) + ' folder and package: '+ name)
        print('Error in saving')
        raise Exception('Error in saving')



def generate_context(Search_Text):
    '''
    This function generates the search context by taking the text being searched as input and returns the text after removing the stop words.

    Input: The text being searched -> Search_Text (In address or any operation _ is used to join the Search_Context)

    Return: Text without stopwords -> Search_Context 
    '''
    # Removing stop words
    stop_words = stopwords.words('english')
    words = Search_Text.split()
    Search_Context = []
    for word in words:
        if word not in stop_words:
            Search_Context.append(word)
    return ' '.join(Search_Context)



def csv_to_df(directory):
    '''
    Input: Takes the address of the csv file -> directory

    The function takes csv file's location and provides the data in a data frame using pandas

    Output: The function returns a data frame which has the data of the different csv(s)
    '''
    # Extracting data from Package_Basic_Data csv
    data = []
    with open(directory,"r") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    df = pd.DataFrame(data) # Creating Dataframe
    df.columns = df.iloc[0] #Setting columns as 1dt row
    df = df.tail(-1)    #Removing 1st row
    return df



def connect_tigergraph(credentials):
    try:
        conn = tg.TigerGraphConnection(
            host = credentials['graph_url'],
            graphname = credentials['graph_name'],
            gsqlSecret = credentials['secret_key']
        )
        auth_token = conn.getToken(credentials['secret_key'])
        return conn,auth_token
    except Exception as e :
        print(e)
        logging.error(f'connect_tigergraph function - Exception: {e}')



def generate_graph_wTG(Search_Context,credentials):
    '''
    Generating the graph by extracting the data from the csv(s) generated and updating on Tiger Graph
    
    Input: Space seperaetd keywords to be searched -> Search_Context (In address or any operation _ is used to join the Search_Context)

    Output: Json response of graph query.
    ''' 
    base_directory = parent_dir + '_'.join(Search_Context.split())
    try:
        # making connection
        conn,auth_token = connect_tigergraph(credentials)

        # commenting these will permit the graph to evolve as more searches are involved
        # Deleting the current graph data
        conn.delVertices("Package")
        conn.delVertices("Programming_Lang")
        conn.delVertices("License")
        conn.delVertices("Dependency_Package")
        conn.delVertices("Dev_Status")

        # Creating list for bulk updatation
        package_vertex, edge_1, edge_2, edge_3, edge_4 = [],[],[],[],[]

        # Extracting data from Package_Basic_Data csv
        df = csv_to_df(base_directory+"/Package_Basic_Data.csv")

        # Adding data tupple in list for updation
        for index in df.index:
            package_vertex.append((df["name"][index], {"author" : df["author"][index],
                                                                "author_email" : df["author_email"][index],
                                                                "dev_status" : df["development_status"][index]}))
            edge_1.append((df["name"][index],df["development_status"][index],{}))
            edge_2.append((df["name"][index],df["license"][index],{}))

        # Extracting data from Package_Prog_Lang csv
        df = csv_to_df(base_directory+"/Package_Prog_Lang.csv")

        # Adding data tupple in list for updation
        for index in df.index:
            edge_3.append((df["name"][index],df["language"][index],{}))
        
        # Extracting data from Package_Dependency csv
        df = csv_to_df(base_directory+"/Package_Dependency.csv")

        # Adding data tupple in list for updation
        for index in df.index:
            edge_4.append((df["name"][index],df["dependency_pkg"][index],{}))
            
        # Adding all the Vertices and Edges to the Tiger Graph
        result = (conn.upsertVertices("Package",package_vertex) and conn.upsertEdges("Package","curr_status","Dev_Status",edge_1)
                and conn.upsertEdges("Package","has_license","License",edge_2) and conn.upsertEdges("Package","used_language","Programming_Lang",edge_3)
                and conn.upsertEdges("Package","has_dependency","Dependency_Package",edge_4))
        if result:
            try:
                print("Graph Generated for "+Search_Context)
                # graph = conn.runInstalledQuery("Stable_Package_Graph_wData")
                graph = conn.runInstalledQuery("Package_Data",params = {"Status":"4%"})
                with open(base_directory+"/graph.json", "w") as graphfile:
                    json.dump(graph[0], graphfile)
                return {"Status Code" : Status_Code["Success"] , "Description" : "Graph generated"}
            except Exception as e:
                print(e)
                return {"Status Code" : Status_Code["Fail"] , "Description" : "Error in graph generation"}
        else:
            print("Error in graph generation")
            logging.error('Error in generating graph for ' + Search_Context)
            return {"Status Code" : Status_Code["Fail"] , "Description" : "Error in graph generation"}
    except Exception as e:
        print(e)
        print("Connection error")
        logging.error(f'generate_graph_wTG function - Exception: {e}')



def generate_graph_wNX(Search_Context):
    '''
    Generating the graph by extracting the data from the csv(s) generated and updating on NetworkX
    
    Input: Space seperaetd keywords to be searched -> Search_Context (In address or any operation _ is used to join the Search_Context)

    Output: GML of the graph
    ''' 
    base_directory = parent_dir+'_'.join(Search_Context.split())
    try:
        # Extracting data from Package_Basic_Data csv
        df = csv_to_df(base_directory+"/Package_Basic_Data.csv")

        G = nx.DiGraph()

        # Adding data tupple in list for updation
        for index in df.index:
            G.add_edge(df["name"][index],df["development_status"][index],label='curr_status')
            G.add_edge(df["name"][index],df["license"][index],label='has_license')
            nx.set_node_attributes(G,{df["name"][index] : {"author" : df["author"][index],
                                                                "author_email" : df["author_email"][index],
                                                                "dev_status" : df["development_status"][index],
                                                                "vertex_type" : "Package"},
                                        df["development_status"][index] : {"vertex_type" : "Development Status"},
                                        df["license"][index] : {"vertex_type" : "License"}})
 
        # Extracting data from Package_Prog_Lang csv
        df = csv_to_df(base_directory+"/Package_Prog_Lang.csv")
        # Adding data tupple in list for updation
        for index in df.index:
            G.add_edge(df["name"][index],df["language"][index],label='used_language')
            nx.set_node_attributes(G,{df["language"][index] : {"vertex_type" : "Programming Language"}})

        # Extracting data from Package_Dependency csv
        df = csv_to_df(base_directory+"/Package_Dependency.csv")
        # Adding data tupple in list for updation
        for index in df.index:
            G.add_edge(df["name"][index],df["dependency_pkg"][index],label='has_dependency')
            nx.set_node_attributes(G,{df["dependency_pkg"][index] : {"vertex_type" : "Dependency Package"}})
        
        nx.write_gml(G, path = parent_dir + '_'.join(Search_Context.split()) + '/graph.gml')

        print("GML generated")
        return {"Status Code" : Status_Code["Success"] , "Description" : "GML generated"}
    #json response
    except Exception as e:
        print(e)
        logging.error(f'generate_graph_wNX function - Exception: {e}')
        return {"Status Code" : Status_Code["Fail"] ,"Description" : "Graph or GML not generated"}



def json_to_gml(Search_Context):
    '''
    Converts json to GML by using loading it to NetworkX
    
    Input: Space seperaetd keywords to be searched -> Search_Context (In address or any operation _ is used to join the Search_Context)

    Output: GML file created from JSON
    ''' 
    G = nx.DiGraph()
    try:
        with open(parent_dir+'_'.join(Search_Context.split())+"/graph.json","r") as graphfile:
            result = json.load(graphfile)
            for package_dependency in result['Package_Dependency']:
                G.add_edge(package_dependency['package'],package_dependency['dependency'],label='has_dependency')
            for license in result['license']:
                G.add_edge(license['package'],license['license'],label='has_license')
            for package_language in result['Package_Language']:
                G.add_edge(package_language['package'],package_language['programming_language'],label='used_language')
        nx.write_gml(G, path = parent_dir + '_'.join(Search_Context.split()) + '/graph.gml')
        return {"Status Code" : Status_Code["Success"] , "Description" : "GML generated"}
    except Exception as e:
        print(e)
        logging.error(f'json_to_gml function - Exception: {e}')
        return {"Status Code" : Status_Code["Fail"] ,"Description" : "GML not generated"}



def update_index(Search_Context, package_count):
    '''
    Updates the index whenever GML and JSON successfully generated. 
    '''
    with open(parent_dir+"index.csv","a",newline='') as file:
        csv_file = csv.writer(file)
        csv_file.writerow(['_'.join(Search_Context.split()),date.today(),package_count])
    print("Index updated")



def gml_to_json(Search_Context):
    base_directory = parent_dir + '_'.join(Search_Context.split())
    try:
        G = nx.read_gml(base_directory+'/graph.gml')
        H = json.dumps(G, default=nx.node_link_data)
        # print(H)
        results = []
        for node in json.loads(H)['nodes']:
            package_data = {}
            if node['vertex_type'] == 'Package':
                package_data['v_id'] = node['id']
                package_data['v_type'] = node['vertex_type']
                package_data['attributes'] = {"author" : node['author'],
                                            "author_email" : node['author_email'],
                                            "dev_status" : node['dev_status']}
                results.append(package_data)
        # print(json.loads(H)['links'])
        package_dependency = []
        license = []
        package_language = []
        for edge in json.loads(H)['links']:
            if edge['label'] == 'has_dependency':
                package_dependency.append({"package": edge['source'], "dependency": edge['target']})
            if edge['label'] == 'has_license':
                license.append({"package": edge['source'], "license": edge['target']})
            if edge['label'] == 'used_language':
                package_language.append({"package": edge['source'], "programming_language": edge['target']})

        with open(base_directory+"/graph.json", "w") as graphfile:
            json.dump({'result':results,'Package_Dependency':package_dependency,'Package_License':license,'Package_Language':package_language}, graphfile)
        
        return {"Status Code" : Status_Code["Success"] ,"Description" : "Json generated"}
    except Exception as e:
        logging.error(f'gml_to_json function - Exception: {e}')
        return {"Status Code" : Status_Code["Fail"] ,"Description" : "Json not generated"}



def fetch_and_update_graph(Search_Context,credentials):
    '''
    Input parameter: Space seperaetd keywords to be searched -> Search_Context (In address or any operation _ is used to join the Search_Context)

    This function performs multiple functionalities:

    1.) Creating list of packages by invoking get_packages function
    2.) Invoking create_directory to create folder at ../library/{Search_Context}
    3.) Sending GET request to fetch the data of all the packages from the list
    4.) Invoking graph_generation to upload the data to TigerGraph and create the Json file of graph

    '''
    init = time()
    # 1. creating directory
    # check for status
    if create_directory(Search_Context)['Status Code'] == 200:
        # 2. Data scrapping required for getting list of packages
        # packages = [*set(get_pypi_packages())]
        packages = get_pypi_packages(Search_Context)
        package_count = 0

        # 3. Getting data of each package in the package list
        for package in packages:
            # Package data in Json format
            try:
                response = (requests.get(pypi_package_data_url + package + '/json')).json()
                # Picking necessary data form Json file
                data = fetch_data(response)
                # Saving data in library
                save_data(Search_Context,data)
                package_count = package_count + 1
            except Exception as e:
                logging.error(f'Response object - Exception: {e}')
                print("Error in response")
                
        # 4. Graph Generation function
        if  credentials['graph_db'] == "TigerGraph":
            if generate_graph_wTG(Search_Context,credentials)['Status Code'] == 200:
                if json_to_gml(Search_Context)['Status Code'] == 200:
                    update_index(Search_Context, package_count)
            
        elif credentials["graph_db"] == "NetworkX":
            if generate_graph_wNX(Search_Context)['Status Code'] == 200:
                if gml_to_json(Search_Context)['Status Code'] == 200:
                    update_index(Search_Context, package_count)

        else:
            logging.error('Credential error - graph_db not configured')
            return {"Status Code" : Status_Code["Fail"] , "Description" : "Credential error - incorrect graph_db"}

    print("Time taken: ",time()-init)



def get_pypi_packages(Search_Context):
    pypi_packages = []
    # Taking 100 Packages from the first 5 pages
    for page in range(1, search_page_range + 1):
        pypi_packages += get_packages(pypi_search_url + '?q=' + '+'.join(Search_Context.split()) + '&page=' + str(page))
    return pypi_packages



def graph(Search_Context):
    '''
    Input: Space seperated text to be searched -> Search_Context (In address or any operation _ is used to join the Search_Context)

    Function checks for the graph file in ../library/{Seach_Context}

    Output: Returns the graph data in json format.
    '''
    try:
        # Creating the base address
        base_directory = parent_dir+'_'.join(Search_Context.split())
        # Seaching for the graph in the base address
        with open(base_directory + "/graph.json", "r") as graphfile:
            return json.load(graphfile) 
    except Exception as e:
        print(e)
        logging.error(f'Graph function - Exception: {e}')
        return "Please check back later."