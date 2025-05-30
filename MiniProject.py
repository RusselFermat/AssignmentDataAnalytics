import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import seaborn as sb

st.title("""Welcome to my Dashboard
And I don't wanna learn another scent""")

with st.sidebar:
    st.header("Configuration")
    api_options = ("echarts", "pyecharts")
    selected_api = st.selectbox(
    label="Choose your preferred API:",
    options=api_options,
    )