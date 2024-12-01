import streamlit as st
from back import waka_gather
import plotly.express as px
import pandas as pd
import json
# Title of the eapp

st.set_page_config(
    page_title='Codestats',
    layout='centered',
)


st.title("Codestats")

if "wakatime_data" not in st.session_state:
    st.session_state.wakatime_data = None

def fetch_wakatime_data():
    d = waka_gather.get_stats()
    langs = d['languanges']
    df = pd.DataFrame(langs)
    print(df)
    st.session_state.wakatime_data = df
    fig = px.pie(df, names='name',values='hours',title='Time spent',hole=.6)
    return fig
st.header("Insert your wakatime api key")
user_input = st.text_input(label='your wakatime api-key')


st.button(label="Fetch wakatime data",on_click=fetch_wakatime_data)
export_data = user_input

if st.session_state.wakatime_data is not None:
    st.subheader("Fetched WakaTime Data")
    fig = fetch_wakatime_data()
    if st.session_state.wakatime_data is not None:
        st.plotly_chart(fig)

df = pd.DataFrame(waka_gather.get_stats()['languanges'])
print(df)
st.dataframe(df)

st.download_button(
    label="Export report as pdf",
    data=export_data,
    file_name="user_input.txt",
    mime="text/plain",
)
