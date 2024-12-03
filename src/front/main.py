import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
from plotly.subplots import make_subplots

# Page config
st.set_page_config(
    page_title='Codestats',
    layout='centered',
)

gitlab_data = requests.get('http://0.0.0.0:8000/stats/gitlab').json()
github_data = requests.get('http://0.0.0.0:8000/stats/github').json()


# Test data
#gitlab_data = {'commits' : 142, 'created issues': 200, 'closed issues': 170}
#github_data = {'total commits' : 512, 'created issues': 200, 'closed issues': 170}

st.title("Codestats")

st.markdown("## 🌟 **Total Contributions Overview**")
total = {
    'commits':gitlab_data['commits'] + github_data['total commits'],
    'created issues': github_data['created issues']+ gitlab_data['created issues'],
    'closed issues': github_data['closed issues'] + gitlab_data['closed issues'],
    'total contributions': sum(github_data.values()) + sum(gitlab_data.values())
}

cols = st.columns(len(total))
for col, (key, value) in zip(cols, total.items()):
    col.metric(label=key, value=value)

cols = st.columns(3)


if "wakatime_data" not in st.session_state:
    st.session_state.wakatime_data = None

st.session_state.os_data = None

def fetch_wakatime_data():
    d = requests.get('http://0.0.0.0:8000/stats/wakatime').json()
    st.session_state.os_data = d['systems']
    langs = d['languanges']
    df = pd.DataFrame(langs)
    df_most_used = df.nlargest(3,'hours')
    df_rest = df[(~df.index.isin(df_most_used.index)) & (df['hours'] > 5)]
    df_most_used.sort_values(ascending=True,inplace=True,by='hours')
    df_rest.sort_values(ascending=True,inplace=True,by='hours')
    st.session_state.wakatime_data = df
    #fig = px.pie(df, names='name',values='hours',title='Time spent',hole=.6)

    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,  # Two rows, one column
        subplot_titles=("Top 3 languanges", "Rest")
    )

    # Plot Rest of the Languages
    fig.add_trace(
        go.Bar(
            x=df_rest["hours"],
            y=df_rest["name"],
            text=df_rest["text"],
            orientation="h",
            marker=dict(color="#FFA07A")
        ),
        row=2,
        col=1
    )

    # Plot Most Used Languages
    fig.add_trace(
        go.Bar(
            x=df_most_used["hours"],
            y=df_most_used["name"],
            text=df_most_used["text"],
            orientation="h",
            marker=dict(color="#90EE90")
        ),
        row=1,
        col=1
    )

    fig.update_xaxes(
        showgrid=True,  # Enable gridlines on x-axis
        gridcolor="lightgray",  # Set gridline color
        gridwidth=1,  # Set gridline thickness
        row=1, col=1
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="lightgray",
        gridwidth=1,
        row=2, col=1
    )

    # Update layout
    fig.update_layout(
        height=700,  # Adjust height for stacked layout
        width=700,   # Keep it proportional
        title="Programming languanges",
        showlegend=False,
        xaxis_title="Hours",
        yaxis_title="Languages",
        title_font_size=24,
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(size=16)
    )

    # Return the figure
    return fig


#st.header("Insert your wakatime api key")
#user_input = st.text_input(label='your wakatime api-key')

fetch_wakatime_data()
#st.button(label="Fetch wakatime data",on_click=fetch_wakatime_data)
#export_data = user_input

if st.session_state.wakatime_data is not None:
    st.subheader("Coding stats")
    data = requests.get('http://0.0.0.0:8000/stats/wakatime/hours').json()
    st.markdown(f"#### **Total hours tracked: {data['time coded']}**")
    st.markdown(f"*Time tracked from {data['start date']}*")


    fig = fetch_wakatime_data()
    if st.session_state.wakatime_data is not None:
        st.plotly_chart(fig,use_container_width=True)
    st.subheader('OS experience')

    d = pd.DataFrame.from_dict(st.session_state.os_data,orient='index')
    pie = px.pie(d, names=d.index,values='percent',hole=0.5, title='Operation systems')
    pie.update_traces(
    text=d['text'],
    textinfo='text+percent',  # Show the custom text and the percentage inside each slice
    textposition='inside',    # Display the custom text inside the slices
    pull=[0.1, 0.1]           # Optional: Make slices slightly "pull" out for better readability
    )

    st.plotly_chart(pie,use_container_width=True)
