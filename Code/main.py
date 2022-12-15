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
    # print(search_context)

    # If data already exist
    with open("library/index.csv","r") as file:
        if '_'.join(search_context.split()) in file.read().split():
            return "We have data already"
    
    # asyn function for fetching data and updation
    background_task.add_task(fetch_and_update,search_context)

    return "Success"