import streamlit as st 
import requests
from constants import *
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(
    page_title="PypiReCom",
)


def main():
    st.title("PypiReCom")
    st.subheader("Package data ready for you!")
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
