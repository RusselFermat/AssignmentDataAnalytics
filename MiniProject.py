import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import seaborn as sb

st.title("""Welcome to my Dashboard
And I don't wanna learn another scent""")

def sidebar():

    # Sidebar title
    st.sidebar.title("Sidebar Menu")

    # Sidebar text input
    name = st.sidebar.text_input("Enter your name")

    # Sidebar selectbox
    option = st.sidebar.selectbox("Choose an option", ["Option A", "Option B", "Option C"])

    # Sidebar slider
    slider_value = st.sidebar.slider("Select a value", 0, 100)

    return name, option, slider_value

result = sidebar()
# Main content
st.snow()
st.write(f"Hello, {result[0]}!")
st.write(f"You selected: {result[1]}")
st.write(f"Slider value: {result[2]}")