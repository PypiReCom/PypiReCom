from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from functions import *
import yaml
from yaml.loader import SafeLoader
from vector_db_functions import *
from fastapi_utils.tasks import repeat_every

app = FastAPI()

@app.on_event("startup")
@repeat_every(seconds=24*60*60)
def vector_db():
    global index 
    vector_db_config = yaml.load(open('Vector_Db_Config.yml'),Loader=SafeLoader)
    df = read_data(parent_dir+"index.csv")
    encode_vectors_and_store(df, vector_db_config['vectors_file_path'])
    loaded_vectors = load_vectors(vector_db_config['vectors_file_path'])
    index = build_index(loaded_vectors)
    # search_context = input("Enter the search context: ")
    # results = perform_search(index, df, search_context)  # Pass df and search_context here
    # print(results.Packages.to_list())

@app.get('/get_graph_file')
def get_graph_file(Search_Text:str):
    Search_Text = Search_Text.lower()
    Search_Context = '_'.join(generate_context(Search_Text).split())
    return FileResponse(path='library/'+Search_Context+'/graph.json',filename=Search_Context+'_Graph.json')

@app.get('/get_gml_file')
def get_gml_file(Search_Text:str):
    Search_Text = Search_Text.lower()
    Search_Context = '_'.join(generate_context(Search_Text).split())
    return FileResponse(path='library/'+Search_Context+'/graph.gml',filename=Search_Context+'_Graph.gml')

@app.get('/get_seach_context_list')
def fetch_search_context():     # Return the list of all the Search Context available in ../library/index.csv
    try:
        search_context_list = []
        date_updated_list = []
        no_of_pkg_list = []
        with open(parent_dir+"index.csv","r") as file:
            for Search_Context in file.read().split():
                search_context_list.append(Search_Context.split(',')[0])
                date_updated_list.append(Search_Context.split(',')[1])
                no_of_pkg_list.append(Search_Context.split(',')[2])
        return {'Search Context':search_context_list,'Date Updated':date_updated_list,'Total Packages':no_of_pkg_list}
    except:
        return "Error in fetching data."

@app.get('/search')
def search_pypi(Search_Text: str, Search_Exact: int, background_task:BackgroundTasks):
    # Generating search context
    Search_Text = Search_Text.lower()
    Search_Context = generate_context(Search_Text)
    credentials = yaml.load(open('Graph_Config.yml'),Loader=SafeLoader)

    # If data already exist
    # Fetching and sending back the json response
    try:
        with open(parent_dir+"index.csv","r") as file:
            for context in file.read().split():
                if '_'.join(Search_Context.split()) in context.split(','):
                    print("We already have the data.")
                    return graph(Search_Context)
    except:
        return "Please check back again"
        
    if Search_Exact == 1:
        # If it is a new Search_Context
        # asyn function for fetching data and updation
        background_task.add_task(fetch_and_update_graph,Search_Context,credentials)
        
        return "Check back after few minutes result is being prepared."
    else:
        df = read_data(parent_dir+"index.csv")
        # search_context = input("Enter the search context: ")
        results = perform_search(index, df, Search_Context)  # Pass df and search_context here
        return {'Suggested Packages': results.Packages.to_list()}
    
@app.get('/comparison_metric')
def compare(Search_Text: str, background_task:BackgroundTasks):
    Search_Text = Search_Text.lower()
    Search_Context = generate_context(Search_Text)
    credentials = yaml.load(open('Graph_Config.yml'),Loader=SafeLoader)

    # If data already exist
    # Fetching and sending back the json response
    try:
        with open(parent_dir+"index.csv","r") as file:
            for context in file.read().split():
                if '_'.join(Search_Context.split()) in context.split(','):
                    print("We already have the data.")
                    pkg_graph = graph(Search_Context)
                    package_dependency_count = {}
                    for package_dependency in pkg_graph['Package_Dependency']:
                        if package_dependency['package'] in package_dependency_count:
                            package_dependency_count[package_dependency['package']] += 1
                        else:
                            package_dependency_count[package_dependency['package']] = 1
                    pkg_graph['Package_Dependency_Count'] = package_dependency_count
                    pkg_names = {'result': get_packages(pypi_search_url + '?q=' + '+'.join(Search_Context.split()))}
                    return {'Pip':pkg_names,'Pypirecom':pkg_graph}
    except:
        return "Please check back again"
    
    background_task.add_task(fetch_and_update_graph,Search_Context,credentials)
    return "Check back after few minutes result is being prepared."