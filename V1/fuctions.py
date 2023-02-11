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
    package_name = response['info']['name'] 
    package_author = response['info']['author'] if response['info']['author'] != None else ''
    package_author_email = response['info']['author_email'] if response['info']['author_email'] != None else ''
    package_license = response['info']['license'] if response['info']['license'] != None else ''
    programming_lang = set()
    package_dev_status = ''
    classifier = response["info"]['classifiers'] if response["info"]['classifiers'] != None else []
    for classifier in response["info"]['classifiers']:
        classifier_list = classifier.split(' :: ')
        if 'Development Status' in classifier_list:
            package_dev_status = classifier_list[-1]
        elif 'Programming Language' in classifier_list:
            programming_lang.add(classifier_list[1])
    package_dependency = set()
    requires_dist = response["info"]['requires_dist'] if response["info"]['requires_dist'] != None else []
    for dependency in requires_dist:
        package_dependency.add(dependency.split()[0])
    
    return [package_name,package_author,package_author_email,package_license,package_dev_status,programming_lang,package_dependency]



def create_directory(Search_Context):
    '''
    Input: Space seperaetd keywords to be searched -> Search_Context (In address or any operation _ is used to join the Search_Context)

    This function creates the folder in ../library named as {Search_Context}

    Then, creates 3 csv(s) in the folder adding the name of attributes/columns in each csv
    '''
    directory = '_'.join(Search_Context.split())
    # Parent Directory path
    parent_dir = "C:/Users/anime/Documents/PypiReCom/V1/library/"
    # Defining the path as ../library/{directory}
    path = os.path.join(parent_dir, directory)
    # Creating the directory
    try:
        os.mkdir(path)
    except:
        print("Folder can not be created.")
        logging.error('Folder can not be created for ' + '_'.join(Search_Context.split()))
        return "Folder can not be created"

    # Creating the differnt csv(s)
    base_directory = "C:/Users/anime/Documents/PypiReCom/V1/library/"+'_'.join(Search_Context.split())
    try:
        with open(base_directory+"/Package_Basic_Data.csv","a", newline='') as file:
            csv_file = csv.writer(file)
            csv_file.writerow(['package_name','package_author','package_author_email','package_license','package_dev_status','search_meta'])
        with open(base_directory+"/Package_Dependency.csv","a", newline='') as file:
            csv_file = csv.writer(file)
            csv_file.writerow(['package_name','dependency_pkg'])
        with open(base_directory+"/Package_Prog_Lang.csv","a", newline='') as file:
            csv_file = csv.writer(file)
            csv_file.writerow(['package_name','language'])
    except:
        print('Error in creating file.')
        logging.error('Error in creating file in ' + '_'.join(Search_Context.split()) + ' folder')
        return "Error in file creation"
    
    return "Folder created"



def save_data(Search_Context,data):
    '''
    Input: Space seperaetd keywords to be searched -> Search_Context (In address or any operation _ is used to join the Search_Context), 
           List of data containing package name,author,email,license,development status,programming language and dependency -> data
    
    This function loads data in 3 csv(s) in the ../library/{Search_Context} and inserts the nessesary data in each csv.
    '''
    # Inserting Data into Different files
    base_directory = "C:/Users/anime/Documents/PypiReCom/V1/library/"+'_'.join(Search_Context.split())
    try:
        # Saving data to files
        package_name,package_author,package_author_email,package_license,package_dev_status,programming_lang,package_dependency = data
        with open(base_directory+"/Package_Basic_Data.csv","a", newline='') as file:
            csv_file = csv.writer(file)
            csv_file.writerow([package_name,package_author,package_author_email,package_license,package_dev_status,''])
        with open(base_directory+"/Package_Dependency.csv","a", newline='') as file:
            csv_file = csv.writer(file)
            for dependency_pkg in package_dependency:
                csv_file.writerow([package_name,dependency_pkg])
        with open(base_directory+"/Package_Prog_Lang.csv","a", newline='') as file:
            csv_file = csv.writer(file)
            for language in programming_lang:
                csv_file.writerow([package_name,language])
    except:
        logging.error('Error in saving data for ' + '_'.join(Search_Context.split()) + ' folder and package: '+ package_name)
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
        logging.error('Connection error')



def generate_graph_wTG(Search_Context,credentials):
    '''
    Generating the graph by extracting the data from the csv(s) generated and updating on Tiger Graoh
    
    Input: Space seperaetd keywords to be searched -> Search_Context (In address or any operation _ is used to join the Search_Context)

    Output: Json response of graph query.
    ''' 
    base_directory = "C:/Users/anime/Documents/PypiReCom/V1/library/"+'_'.join(Search_Context.split())
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
            package_vertex.append((df["package_name"][index], {"author" : df["package_author"][index],
                                                                "author_email" : df["package_author_email"][index],
                                                                "dev_status" : df["package_dev_status"][index],
                                                                "search_meta" : df["search_meta"][index]}))
            edge_1.append((df["package_name"][index],df["package_dev_status"][index],{}))
            edge_2.append((df["package_name"][index],df["package_license"][index],{}))

        # Extracting data from Package_Prog_Lang csv
        df = csv_to_df(base_directory+"/Package_Prog_Lang.csv")

        # Adding data tupple in list for updation
        for index in df.index:
            edge_3.append((df["package_name"][index],df["language"][index],{}))
        
        # Extracting data from Package_Dependency csv
        df = csv_to_df(base_directory+"/Package_Dependency.csv")

        # Adding data tupple in list for updation
        for index in df.index:
            edge_4.append((df["package_name"][index],df["dependency_pkg"][index],{}))
            
        # Adding all the Vertices and Edges to the Tiger Graph
        result = (conn.upsertVertices("Package",package_vertex) and conn.upsertEdges("Package","curr_status","Dev_Status",edge_1)
                and conn.upsertEdges("Package","has_license","License",edge_2) and conn.upsertEdges("Package","used_language","Programming_Lang",edge_3)
                and conn.upsertEdges("Package","has_dependency","Dependency_Package",edge_4))
        if result:
            print("Graph Generated for "+Search_Context)
            graph = conn.runInstalledQuery("Stable_Package_Graph_wData")
            with open(base_directory+"/graph.json", "w") as graphfile:
                json.dump(graph[0], graphfile)
            return "Graph generated"
        else:
            print("Error in graph generation")
            logging.error('Error in generating graph for ' + Search_Context)
            return "Error in graph generation"
    except Exception as e:
        print(e)
        print("Connection error")



def generate_graph_wNX(Search_Context):
    base_directory = "C:/Users/anime/Documents/PypiReCom/V1/library/"+'_'.join(Search_Context.split())
    try:
        # Extracting data from Package_Basic_Data csv
        df = csv_to_df(base_directory+"/Package_Basic_Data.csv")

        G = nx.DiGraph()

        # Adding data tupple in list for updation
        for index in df.index:
            G.add_edge(df["package_name"][index],df["package_dev_status"][index],label='curr_status')
            G.add_edge(df["package_name"][index],df["package_license"][index],label='has_license')
            nx.set_node_attributes(G,{df["package_name"][index] : {"author" : df["package_author"][index],
                                                                "author_email" : df["package_author_email"][index],
                                                                "dev_status" : df["package_dev_status"][index],
                                                                "search_meta" : df["search_meta"][index],
                                                                "vertex_type" : "Package"},
                                        df["package_dev_status"][index] : {"vertex_type" : "Development Status"},
                                        df["package_license"][index] : {"vertex_type" : "License"}})
 
        # Extracting data from Package_Prog_Lang csv
        df = csv_to_df(base_directory+"/Package_Prog_Lang.csv")
        # Adding data tupple in list for updation
        for index in df.index:
            G.add_edge(df["package_name"][index],df["language"][index],label='used_language')
            nx.set_node_attributes(G,{df["language"][index] : {"vertex_type" : "Programming Language"}})

        # Extracting data from Package_Dependency csv
        df = csv_to_df(base_directory+"/Package_Dependency.csv")
        # Adding data tupple in list for updation
        for index in df.index:
            G.add_edge(df["package_name"][index],df["dependency_pkg"][index],label='has_dependency')
            nx.set_node_attributes(G,{df["dependency_pkg"][index] : {"vertex_type" : "Dependency Package"}})
        
        nx.write_gml(G, path="C:/Users/anime/Documents/PypiReCom/V1/library/"+'_'.join(Search_Context.split())+'/graph.gml')

        print("Graph & GML generated")
        return "Graph & GML generated"
    #json response
    except Exception as e:
        print(e)



def json_to_gml(Search_Context):
    G = nx.DiGraph()
    color = []
    try:
        # print("C:/Users/anime/Documents/PypiReCom/V1/library/"+'_'.join(Search_Context.split())+"/graph.json")
        with open("C:/Users/anime/Documents/PypiReCom/V1/library/"+'_'.join(Search_Context.split())+"/graph.json","r") as graphfile:
            result = json.load(graphfile)
            for package_dependency in result['Package_Dependency']:
                G.add_node(package_dependency['package'], color='red')
                color.append('red')
                G.add_node(package_dependency['dependency'], color='blue')
                color.append('blue')
                G.add_edge(package_dependency['package'],package_dependency['dependency'],label='has_dependency')
                # graph.node(package_dependency['package'],shape='doublecircle')
                # graph.edge(package_dependency['package'],package_dependency['dependency'],label='has_dependency')
            for package_license in result['Package_License']:
                G.add_node(package_license['license'], color='green')
                color.append('green')
                G.add_edge(package_license['package'],package_license['license'],label='has_license')
                # graph.edge(package_license['package'],package_license['license'],label='has_license')
            for package_language in result['Package_Language']:
                G.add_node(package_language['programming_language'], color='pink')
                color.append("pink")
                G.add_edge(package_language['package'],package_language['programming_language'],label='used_language')
                # graph.edge(package_language['package'],package_language['programming_language'],label='used_language')
        nx.write_gml(G, path="C:/Users/anime/Documents/PypiReCom/V1/library/"+'_'.join(Search_Context.split())+'/graph.gml')
        return "GML generated"
    except Exception as e:
        print(e)
        return ("GML not generated")



def update_index(Search_Context, package_count):
    with open("C:/Users/anime/Documents/PypiReCom/V1/library/index.csv","a",newline='') as file:
        csv_file = csv.writer(file)
        csv_file.writerow(['_'.join(Search_Context.split()),date.today(),package_count])
    print("Index updated")



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
    # 1
    # Data scrapping required for getting list of packages
    packages = []
    # Taking 100 Packages from the first 5 pages
    for page in range(1,6):
        packages += get_packages('https://pypi.org/search/?q=' + '+'.join(Search_Context.split()) + '&page=' + str(page))

    package_count = 0
    
    # 2. creating directory
    if create_directory(Search_Context) == "Folder created":
        # check for status
        # 3. Getting data of each package in the package list
        for package in packages:
            # Package data in Json format
            try:
                response = (requests.get('https://pypi.python.org/pypi/'+package+'/json')).json()
                # Picking nesseary data form Json file
                data = fetch_data(response)
                # Saving data in library
                save_data(Search_Context,data)
                package_count = package_count + 1
            except:
                print("Error in response")
    
    # 4. Graph Generation function
    if  credentials['graph_db'] == "TigerGraph":
        if generate_graph_wTG(Search_Context,credentials) == "Graph generated" and json_to_gml(Search_Context) == "GML generated":
            update_index(Search_Context, package_count)
        
    elif credentials["graph_db"] == "NetworkX":
        if generate_graph_wNX(Search_Context) == "Graph & GML generated":
            update_index(Search_Context, package_count)
    
    else:
        logging.error('Credential error - graph_db not configured')
        return "Credential error - incorrect graph_db"
    
    print("Time taken: ",time()-init)



def graph(Search_Context):
    '''
    Input: Space seperated text to be searched -> Search_Context (In address or any operation _ is used to join the Search_Context)

    Function checks for the graph file in ../library/{Seach_Context}

    Output: Returns the graph data in json format.
    '''
    try:
        # Creating the base address
        base_directory = "C:/Users/anime/Documents/PypiReCom/V1/library/"+'_'.join(Search_Context.split())
        # Seaching for the graph in the base address
        with open(base_directory+"/graph.json", "r") as graphfile:
            return json.load(graphfile) 
    except Exception as e:
        print(e)
        return "Please check back later."