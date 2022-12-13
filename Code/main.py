from fastapi import FastAPI
import requests
import csv
import json
from fuctions import *

app = FastAPI()

packages = []

def get_search_context():
    pass

@app.get('/search/')
def search_pypi(Search_Text: str):
    Search_Text = '_'.join(Search_Text.split())
    # If data already exist
    with open("library/index.csv","r") as file:
        if Search_Text in file.read().split():
            return "We have data already"
    with open("library/index.csv","a",newline='') as file:
        csv_file = csv.writer(file)
        csv_file.writerow([Search_Text])

    # Data scrapping required for getting list of packages
    packages = get_packages('https://pypi.org/search/?q='+'+'.join(Search_Text.split()))
    print(packages)
    # creating directory
    create_directory(Search_Text)
    # Getting data of each package in the package list
    for package in packages:
        # Package data in Json format
        print(package)
        try:
            response = (requests.get('https://pypi.python.org/pypi/'+package+'/json')).json()
            # print(response)
            # Picking nesseary data form Json file
            data = fetch_data(response)
            # print(data)
            # Saving data in library
            save_data(Search_Text,data)
            # return "Success"
        except:
            print("Error in response")
    
    return "Success"