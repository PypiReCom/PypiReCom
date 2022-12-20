from fastapi import FastAPI, BackgroundTasks
import requests
import csv
import json
from fuctions import *

app = FastAPI()

packages = []

@app.get('/search/')
async def search_pypi(search_text: str, background_task:BackgroundTasks):
    # Generating search context
    search_context = generate_context(search_text)

    # If data already exist
    # Fetching and sending back the json response
    try:
        with open("library/index.csv","r") as file:
            if '_'.join(search_context.split()) in file.read().split():
                print("We already have the data.")
                return graph(search_context)
    except:
        return "Please check back again"

    # asyn function for fetching data and updation
    background_task.add_task(fetch_and_update_graph,search_context)
    
    return "Check back after few minutes result is being prepared."