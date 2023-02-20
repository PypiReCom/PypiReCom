import streamlit as st 
import requests
from constants import *
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb


st.set_page_config(
    page_title="PypiReCom",
)


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
    # st.title("PypiReCom")
    footer()
    st.image(Image.open('PypiReCom Logo.png'),width=300)
    st.subheader("Package data ready for you!")
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
    col1,col2,col3,col4 = st.columns([2,1,1,1])

    result = requests.get(api_endpoint + '/get_seach_context_list').json()
    # st.write(result)
    col1.write("Search Context")
    col2.write("Date Updated")
    col3.write("Total Packages")
    button = []
    search_text = []
    for index in range(len(result['Search Context'])):
        col1,col2,col3,col4 = st.columns([2,1,1,1])
        search_text.append(' '.join(result['Search Context'][index].split('_')).title())
        col1.write(search_text[index])
        col2.write(result['Date Updated'][index])
        col3.write(result['Total Packages'][index])
        button.append(col4.button(label='Search',key='button_'+str(index)))
        if button[index]:
            st.session_state['search_text'] = search_text[index]
            switch_page("Search Package")
            


main()
