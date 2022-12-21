from fastapi import FastAPI, BackgroundTasks
import requests
import csv
import json
from fuctions import *
import yaml
from yaml.loader import SafeLoader

app = FastAPI()

@app.get('/get_seach_context_list/')
def fetch_search_context():     # Return the list of all the Search Context available in ../library/index.csv
    try:
        search_context_list = []
        with open("library/index.csv","r") as file:
            for Search_Context in file.read().split():
                search_context_list.append({'Search Context' : Search_Context.split(',')[0],
                                            'Date Updated' : Search_Context.split(',')[1]})
        return search_context_list
    except:
        return "Error in fetching data."

@app.get('/search/')
async def search_pypi(Search_Text: str, background_task:BackgroundTasks):
    # Generating search context
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