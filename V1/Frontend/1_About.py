import streamlit as st

st.set_page_config(
    page_title="PypiReCom",
)

def main():
    st.title('PypiReCom')
    st.subheader('About')
    st.sidebar.success("Select a page to start.")
    if 'search_text' not in st.session_state:
        st.session_state['search_text'] = ''
    st.write("Visit Our [GitHub](https://github.com/Animesh2210/PypiReCom)")
    st.write("Major Contributors: [Dr. Shyam Sundaram](https://www.linkedin.com/in/bioenable) & [Animesh Verma](https://www.linkedin.com/in/animesh2210)")

if __name__ == "__main__":
    main()