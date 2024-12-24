import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("https://raw.githubusercontent.com/noxzym/bike-sharing-dicoding-data-analyst/refs/heads/main/dashboard/main_data.csv")

st.write(df)