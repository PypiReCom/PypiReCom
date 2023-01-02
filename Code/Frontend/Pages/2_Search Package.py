import streamlit as st
import requests
from constants import * 
import graphviz

st.set_page_config(
    page_title="PypiReCom"
)

def search_package(search_url):
    return requests.get(search_url).json()

def main():
    #basic page
    if 'search_text' not in st.session_state:
        st.session_state['search_text'] = ''
    st.title("PypiReCom")
    st.subheader("Get the perfect python package for you!")
    with st.form(key='Search_Package_Form'):
        nav1,nav2 = st.columns([5,1])

        with nav1:
            search_text = st.text_input("Search for:",st.session_state['search_text'])

        with nav2:
            st.text("Search")
            search_button = st.form_submit_button(label='Search')
        
    #result
    if search_button:
        search_url = api_endpoint + '/search?Search_Text=' + search_text
        result = search_package(search_url)
        if type(result) == str:
            st.write(result)
        else:
            st.success("Showing results for " + search_text)
            st.subheader("Knowledge Graph")
            graph = graphviz.Digraph()
            graph.attr('node', size = '2,2')
            for package_dependency in result['Package_Dependency']:
                graph.node(package_dependency['package'],shape='doublecircle')
                graph.edge(package_dependency['package'],package_dependency['dependency'],label='has_dependency')
            for package_license in result['Package_License']:
                graph.edge(package_license['package'],package_license['license'],label='has_license')
            for package_language in result['Package_Language']:
                graph.edge(package_language['package'],package_language['programming_language'],label='used_language')
            file = requests.get(api_endpoint + '/get_graph_file?Search_Text=' + search_text).content
            st.download_button("Download Graph Json",data=file,file_name='Graph.json')
            st.write(graph)
            # st.download_button("Download Graph Image",data=graph.render(format='png'))
            
            pkg_name,author,author_email,dev_status = st.columns(4)
            pkg_name.write("Package Name")
            author.write("Author")
            author_email.write("Author Email")
            dev_status.write("Development Status")
            packages = result['result']
            for package in packages:
                pkg_name,author,author_email,dev_status = st.columns(4)
                pkg_name.write(package['v_id'])
                author.write(package['attributes']['author'])
                author_email.write(package['attributes']['author_email'])
                dev_status.write(package['attributes']['dev_status'])


main()