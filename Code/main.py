from fastapi import FastAPI
import requests
import csv
import json
from fuctions import *
from tqdm import tqdm

app = FastAPI()

packages = []

@app.get('/search/')
def search_pypi(search_text: str):
    # Generating search context
    search_context = generate_context(search_text)
    # print(search_context)

    # If data already exist
    with open("library/index.csv","r") as file:
        if '_'.join(search_context.split()) in file.read().split():
            return "We have data already"
    # asyn function for fetching data and updation
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
    for package in tqdm(packages):
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
    
    return "Success"