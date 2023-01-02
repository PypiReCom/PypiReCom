from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
import requests
import csv
import json
from fuctions import *
import yaml
from yaml.loader import SafeLoader

app = FastAPI()

@app.get('/get_graph_file')
def get_file(Search_Text:str):
    Search_Text = Search_Text.lower()
    Search_Context = '_'.join(generate_context(Search_Text).split())
    return FileResponse(path='library/'+Search_Context+'/graph.json',filename=Search_Context+'_Graph.json')

@app.get('/get_seach_context_list')
def fetch_search_context():     # Return the list of all the Search Context available in ../library/index.csv
    try:
        search_context_list = []
        date_updated_list = []
        no_of_pkg_list = []
        with open("library/index.csv","r") as file:
            for Search_Context in file.read().split():
                search_context_list.append(Search_Context.split(',')[0])
                date_updated_list.append(Search_Context.split(',')[1])
                no_of_pkg_list.append(Search_Context.split(',')[2])
        return {'Search Context':search_context_list,'Date Updated':date_updated_list,'Total Packages':no_of_pkg_list}
    except:
        return "Error in fetching data."

@app.get('/search')
def search_pypi(Search_Text: str, background_task:BackgroundTasks):
    # Generating search context
    Search_Text = Search_Text.lower()
    Search_Context = generate_context(Search_Text)
    credentials = yaml.load(open('TigerGraph_SecretKey.yml'),Loader=SafeLoader)

    # If data already exist
    # Fetching and sending back the json response
    try:
        with open("library/index.csv","r") as file:
            for context in file.read().split():
                if '_'.join(Search_Context.split()) in context.split(','):
                    print("We already have the data.")
                    return graph(Search_Context)
    except:
        return "Please check back again"
    
    # If it is a new Search_Context
    # asyn function for fetching data and updation
    background_task.add_task(fetch_and_update_graph,Search_Context,credentials)
    
    return "Check back after few minutes result is being prepared."