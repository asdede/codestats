import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import pandas as pd
import plotly.io as pio

base_url = 'http://api:8000'
#base_url = 'http://0.0.0.0:8000'

def create_wakatime_plot():
    d = requests.get(f'{base_url}/stats/wakatime').json()
    langs = d['languanges']
    df = pd.DataFrame(langs)
    df_most_used = df.nlargest(3,'hours')
    df_rest = df[(~df.index.isin(df_most_used.index)) & (df['hours'] > 5)]
    df_most_used.sort_values(ascending=True,inplace=True,by='hours')
    df_rest.sort_values(ascending=True,inplace=True,by='hours')

    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,  # Two rows, one column
        subplot_titles=("Top 3 Languages", "Rest")
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
        height=600,  # Adjust height for stacked layout
        width=750,   
        title="",
        showlegend=False,
        xaxis_title="Hours",
        yaxis_title="",
        title_font_size=24,
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(size=12)
    )
    # Save the figure as an image (PNG format)
    fig.write_image("wakatime_plot.png")  # You can change the format here (e.g., .jpg, .pdf)
