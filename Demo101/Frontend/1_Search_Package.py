import streamlit as st
import requests
from constants import * 
import graphviz
from PIL import Image
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb

st.set_page_config(
    page_title="PypiReCom"
)

def search_package(search_url):
    return requests.get(search_url).json()

def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="White",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():
    myargs = [
        """
        <p>
        Made with ❤️ by 
        <a href="https://www.linkedin.com/in/bioenable" target="_blank">Dr. Shyam Sundaram</a>,
        <a href="https://www.linkedin.com/in/animesh2210" target="_blank">Animesh Verma</a> &
        <a href="https://www.linkedin.com/in/avs-sridhar-8b9904176/" target="_blank">Sridhar Aluru</a>
        </p>
        """
    ]
    layout(*myargs)

def main():
    #basic page
    if 'search_text' not in st.session_state:
        st.session_state['search_text'] = ''
    # st.title("PypiReCom")
    footer()
    # with st.sidebar:
    #     st.header('Contributers')
    #     st.markdown("""
    #     **Dr. Shyam Sundaram**
    #     - [LinkedIn](https://www.linkedin.com/in/bioenable)
    #     - [Github](https://github.com/drshyamsundaram)
    #     """)
    #     st.markdown("""
    #     **Animesh Verma**
    #     - [LinkedIn](https://www.linkedin.com/in/animesh2210)
    #     - [Github](https://github.com/Animesh2210)
    #     """)
    st.image(Image.open('PypiReCom_Logo.png'),width=300)
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
            try:
                json_file = requests.get(api_endpoint + '/get_graph_file?Search_Text=' + search_text).content
                if json_file.decode('ascii') == 'Internal Server Error':
                    raise Exception('Json file not available.')
                st.download_button("Download Graph Json",data=json_file,file_name=search_text+'_Graph.json')
            except:
                pass
            try:
                gml_file = requests.get(api_endpoint + '/get_gml_file?Search_Text=' + search_text).content
                if gml_file.decode('ascii') == 'Internal Server Error':
                    raise Exception('GML file not available.')
                st.download_button("Download Graph GML",data=gml_file,file_name=search_text+'_Graph.gml')
            except Exception as e:
                pass
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
