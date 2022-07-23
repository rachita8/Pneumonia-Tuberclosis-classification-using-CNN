import streamlit as st
import app1
import app2
import app3

hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
                
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

PAGES = {
    "Tuberculosis and Pneumonia Detection": app1,
    "Forum Page": app2,
    "Remedies and Hospital search": app3,
}

st.sidebar.title('Navigation')
selection = st.sidebar.selectbox("Navigate to", list(PAGES.keys()))
page = PAGES[selection]
page.app()