from bs4 import BeautifulSoup
import requests
import csv
import os
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

def get_packages(link):
    packages = []
    soup = BeautifulSoup(requests.get(link).content,'html.parser')
    html_data = soup.find_all('a',class_="package-snippet")
    for package in html_data:
        packages.append(str(package).split('/')[2])
    return packages

# def check_data(data):
#     if data == None:
#         return ''
#     return data

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