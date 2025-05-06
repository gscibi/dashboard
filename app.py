import streamlit as st
import pandas as pd
import plotly.express as px
from helpers import *

df = pd.read_csv('sales.csv')
df = data_cleaning(df)
st.title("Analytics Dashboard")

#### plot
st.header("Sales Over Time")
plot_sales_over_time(df)

#### plot 2
st.header("Sales by Region")
plot_sales_by_country(df)