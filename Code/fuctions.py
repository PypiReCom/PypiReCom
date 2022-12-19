from bs4 import BeautifulSoup
import requests
import csv
import os
import nltk
import pandas as pd
import json
nltk.download('stopwords')
from nltk.corpus import stopwords
import pyTigerGraph as tg

def get_packages(link):
    packages = []
    soup = BeautifulSoup(requests.get(link).content,'html.parser')
    html_data = soup.find_all('a',class_="package-snippet")
    for package in html_data:
        packages.append(str(package).split('/')[2])
    return packages

def fetch_data(response):
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

def create_directory(search_context):
    directory = '_'.join(search_context.split())
    # Parent Directory path
    parent_dir = "C:/Users/anime/Documents/PypiReCom/Code/library/"
    # Path
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    ##
    base_directory = "library/"+'_'.join(search_context.split())
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
        print('Error in creating file')


def save_data(search_context,data):
    # Inserting Data into Different files
    base_directory = "library/"+'_'.join(search_context.split())
    try:
        # Saving data to file
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
        print('Error in saving')

def generate_context(search_text):
    # Removing stop words
    stop_words = stopwords.words('english')
    words = search_text.split()
    search_context = []
    for word in words:
        if word not in stop_words:
            search_context.append(word)
    return ' '.join(search_context)

def fetch_and_update_graph(search_context):     #description
    with open("library/index.csv","a",newline='') as file:
        csv_file = csv.writer(file)
        csv_file.writerow(['_'.join(search_context.split())])
        
    # offline process
    # Data scrapping required for getting list of packages
    packages = []
    for page in range(1,6):
        packages += get_packages('https://pypi.org/search/?q=' + '+'.join(search_context.split()) + '&page=' + str(page))
    # print(len(packages))

    # creating directory
    create_directory(search_context)
    
    # Getting data of each package in the package list
    for package in packages:
        # Package data in Json format
        # print(package)
        try:
            response = (requests.get('https://pypi.python.org/pypi/'+package+'/json')).json()
            # print(response)
            # Picking nesseary data form Json file
            data = fetch_data(response)
            # print(data)
            # Saving data in library
            save_data(search_context,data)
            # return "Success"
        except:
            print("Error in response")
    
    # Graph Generation function
    generate_graph(search_context)
    # return "Success"

def generate_graph(search_context):     # 
    base_directory = "library/"+'_'.join(search_context.split())
    # try catch
    # making connection
    conn = tg.TigerGraphConnection(
        host='https://cab6c8c57c1140ac9283258d135b57d6.i.tgcloud.io',
        graphname='Test',
        gsqlSecret='elgabddfotvdu68tgmq0b79d6a1pqevh',
    )
    auth_token = conn.getToken('elgabddfotvdu68tgmq0b79d6a1pqevh')
    conn.delVertices("Package")
    conn.delVertices("Programming_Lang")
    conn.delVertices("License")
    conn.delVertices("Dependency_Package")
    conn.delVertices("Dev_Status")
    # print(auth_token)
    # print(conn.getSchema())
    package_vertex = []
    edge_1 = []
    edge_2 = []
    edge_3 = []
    edge_4 = []

    data = []
    with open(base_directory+"/Package_Basic_Data.csv","r") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    # print(l)
    df = pd.DataFrame(data)
    df.columns = df.iloc[0]
    df = df.tail(-1)
    # print(df)
    for index in df.index:
        # print(df["package_name"][index],df["package_author"][index])
        # conn.upsertVertex("Package",df["package_name"][index], {"author" : df["package_author"][index],
        #                                                         "author_email" : df["package_author_email"][index],
        #                                                         "dev_status" : df["package_dev_status"][index],
        #                                                         "search_meta" : df["search_meta"][index]})
        package_vertex.append((df["package_name"][index], {"author" : df["package_author"][index],
                                                                "author_email" : df["package_author_email"][index],
                                                                "dev_status" : df["package_dev_status"][index],
                                                                "search_meta" : df["search_meta"][index]}))
        # conn.upsertVertices
        # conn.upsertVertex("Dev_Status",df["package_dev_status"][index], {})
        # conn.upsertVertex("License",df["package_license"][index], {})
        # conn.upsertEdge("Package",df["package_name"][index],"curr_status","Dev_Status",df["package_dev_status"][index],{})
        # conn.upsertEdge("Package",df["package_name"][index],"has_license","License",df["package_license"][index],{})
        edge_1.append((df["package_name"][index],df["package_dev_status"][index],{}))
        edge_2.append((df["package_name"][index],df["package_license"][index],{}))
    # print(package_vertex)

    data = []
    with open(base_directory+"/Package_Prog_Lang.csv","r") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    # print(data)
    df = pd.DataFrame(data)
    df.columns = df.iloc[0]
    df = df.tail(-1)
    for index in df.index:
        # conn.upsertVertex("Programming_Lang",df["package_license"][index], {})
        # conn.upsertEdge("Package",df["package_name"][index],"used_language","Programming_Lang",df["language"][index],{})
        edge_3.append((df["package_name"][index],df["language"][index],{}))
    
    data = []
    with open(base_directory+"/Package_Dependency.csv","r") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    # print(data)
    df = pd.DataFrame(data)
    df.columns = df.iloc[0]
    df = df.tail(-1)
    for index in df.index:
        # conn.upsertVertex("Dependency_Package",df["dependency_pkg"][index], {}) 
        # conn.upsertEdge("Package",df["package_name"][index],"has_dependency","Dependency_Package",df["dependency_pkg"][index],{})
        edge_4.append((df["package_name"][index],df["dependency_pkg"][index],{}))

    result = (conn.upsertVertices("Package",package_vertex) and conn.upsertEdges("Package","curr_status","Dev_Status",edge_1)
            and conn.upsertEdges("Package","has_license","License",edge_2) and conn.upsertEdges("Package","used_language","Programming_Lang",edge_3)
            and conn.upsertEdges("Package","has_dependency","Dependency_Package",edge_4))
    if result:
        print("Graph Generated for "+search_context)
        graph = conn.runInstalledQuery("Stable_packages")
        print(type(graph[0]))
        with open(base_directory+"/graph.json", "w") as graphfile:
            json.dump(graph[0], graphfile)
    else:
        print("Error in graph generation.")
    # elgabddfotvdu68tgmq0b79d6a1pqevh

def graph(search_context):
    base_directory = "library/"+'_'.join(search_context.split())
    with open(base_directory+"/graph.json", "r") as graphfile:
        return json.load(graphfile) 