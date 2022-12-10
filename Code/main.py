from fastapi import FastAPI
import requests
import csv
import json

app = FastAPI()

package_list = ['torch']

@app.get('/search/')
def search_pypi(Search_Text: str):
    # response = (requests.get('https://pypi.org/search/?q='+search_Text).text)
    # Data scrapping required for getting list of packages

    # Getting data of each package in the package list
    for package in package_list:
        # Package data in Json format
        response = (requests.get('https://pypi.python.org/pypi/'+package+'/json')).json()

        # Picking nesseary data form Json file
        package_name = response['info']['name']
        package_author = response['info']['author']
        package_author_email = response['info']['author_email']
        package_license = response['info']['license']
        programming_lang = set()
        for classifier in response["info"]['classifiers']:
            classifier_list = classifier.split(' :: ')
            if 'Development Status' in classifier_list:
                package_dev_status = classifier_list[-1]
            elif 'Programming Language' in classifier_list:
                programming_lang.add(classifier_list[1])
        package_dependency = set()
        for dependency in response['info']['requires_dist']:
            package_dependency.add(dependency.split()[0])

        # Inserting Data into Different files
        try:
            with open("Package_Basic_Data.csv","a", newline='') as file:
                csv_file = csv.writer(file)
                csv_file.writerow([package_name,package_author,package_author_email,package_license,package_dev_status,''])
            with open("Package_Dependency.csv","a", newline='') as file:
                csv_file = csv.writer(file)
                for dependency_pkg in package_dependency:
                    csv_file.writerow([package_name,dependency_pkg])
            with open("Package_Prog_Lang.csv","a", newline='') as file:
                csv_file = csv.writer(file)
                for language in programming_lang:
                    csv_file.writerow([package_name,language])
        except:
            print('Error')
        return(response)
