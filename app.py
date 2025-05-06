import streamlit as st
import pandas as pd
import plotly.express as px
from helpers import *

df = pd.read_csv('sales.csv')
df = data_cleaning(df)
st.title("Analytics Dashboard")

#### plot
plot_sales_over_time(df)
