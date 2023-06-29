import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb
from constants import *


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
    footer()
    st.image(Image.open(logo_path),width=300)
    st.subheader("Credits:")
    
    col1,col2,col3 = st.columns([1,1,1])
    col1.image(Image.open('Contributing Libraries/bs4.png'))
    col2.image(Image.open('Contributing Libraries/fastapi.png'))
    col3.image(Image.open('Contributing Libraries/graphviz.png'))

    col1,col2,col3 = st.columns([1,1,1])
    col1.image(Image.open('Contributing Libraries/networkx.png'))
    col2.image(Image.open('Contributing Libraries/pandas.png'))
    col3.image(Image.open('Contributing Libraries/pytigergraph.png'))
    
    col1,col2,col3 = st.columns([1,1,1])
    col1.image(Image.open('Contributing Libraries/requests.jpg'))
    col2.image(Image.open('Contributing Libraries/streamlit.png'))
    col3.image(Image.open('Contributing Libraries/yaml.png'))
    
main()
