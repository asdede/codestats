import streamlit as st
from PIL import Image
icon = Image.open('favicon.ico')
st.set_page_config(
    page_title='Codestats',
    layout='centerd',
    initial_sidebar_state='auto'
)
