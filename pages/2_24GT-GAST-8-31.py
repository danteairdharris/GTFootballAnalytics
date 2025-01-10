import streamlit as st 
import pandas as pd 
import os
import numpy as np
import matplotlib.pyplot as plt
import base64
import plotly.graph_objects as go
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.metric_cards import style_metric_cards

st.set_page_config(layout='wide')

# Define notes file path
notes_file_path = "notes.txt"

data = pd.read_csv('./data/GAST-GT-08-31-24-PLAYS')

#region functions

# Read notes from the file
def load_notes(file_path):
    try:
        with open(file_path, "r") as file:
            notes = file.readlines()
            return [note.strip() for note in notes]
    except FileNotFoundError:
        return ["Notes file not found. Please check the file path."]

def get_image_as_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

def create_circular_progress_bar(percentage, title_input, color_input):
    # Ensure a fresh figure every time
    fig = go.Figure()

    # Determine the color based on input
    color = '#0afa46' if color_input == 'green' else (
        '#2499ff' if color_input == 'blue' else '#e38c00'
    )


    # Add a full circle for the background
    fig.add_trace(go.Pie(
        values=[1],
        hole=0.7,
        marker_colors=['#e6e5e3'],
        showlegend=False,
        textinfo='none'
    ))

    # Add a partial circle for the progress
    fig.add_trace(go.Pie(
        values=[percentage, 100-percentage],  # Correctly map progress and remainder
        hole=0.7,
        marker=dict(
            colors=[color, 'rgba(0,0,0,0)'],  # Progress color and transparent remainder
            line=dict(color='black', width=1)  # Black outline
        ),
        direction='clockwise',
        rotation=0,  # Start from the top of the circle
        showlegend=False,
        textinfo='none'
    ))

    # Update layout to make the background transparent and add a title
    fig.update_layout(
        title={
            'text': f"{title_input}: {percentage}%",
            'y': 0.95,  # Position the title closer to the top
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'color': 'gray',  # Gray color for the title
                'size': 12        # Smaller font size
            }
        },
        margin=dict(t=20, b=5, l=0, r=0),
        width=100,  # Adjust size for better alignment
        height=100,
        paper_bgcolor="rgba(0,0,0,0)"  # Transparent background
    )

    return fig

def create_semi_circular_gauge(percentage, title_input, color_input):
    # Determine the color based on input
    color = '#0afa46' if color_input == 'green' else (
        '#2499ff' if color_input == 'blue' else '#e38c00'
    )

    # Create a semi-circular gauge
    fig = go.Figure()

    # Add the gauge
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=percentage,
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': color},  # Progress bar color
            'bgcolor': "white",  # Background color
            'steps': [
                {'range': [0, 100], 'color': '#e6e5e3'}  # Background color for gauge
            ],
            'threshold': {
                'line': {'color': color, 'width': 4},
                'thickness': 0.75,
                'value': percentage
            }
        }
    ))

    # Update layout for a semi-circle effect
    fig.update_layout(
        margin=dict(t=5, b=5, l=5, r=5),
        width=100,
        height=75,
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent background
    )

    return fig

#endregion

header = st.container()
header_cols = header.columns(5)
notes = load_notes(notes_file_path)
    
with header_cols[0].popover('ℹ️Info', use_container_width=True):
    for note in notes:
        st.warning('* '+note)

                

          