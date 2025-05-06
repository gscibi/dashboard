import streamlit as st
import pandas as pd
import plotly.express as px
from helpers import *

df = pd.read_csv('sales.csv')
df = data_cleaning(df)
st.title("Analytics Dashboard")

st.markdown("""
    **Created by:** [Gianluca Scibilia]
    **Description:**
    This Streamlit app visualizes sales data through interactive charts.

    Features include:
    - Sales over time
    - Sales by country/region
    - Sales by product
    - Sales by country
    - Performance comparison between multiple salespeople
    github repo: https://github.com/gscibi/dashboard
""")

st.sidebar.title("Navigation")
show_time = st.sidebar.checkbox("📈 Sales Over Time", True)
show_region = st.sidebar.checkbox("🌍 Sales by Region", True)
show_top = st.sidebar.checkbox("🥇 Top Product Sales", True)
show_country = st.sidebar.checkbox("📊 Sales by Country", True)
show_comparison = st.sidebar.checkbox("🧑‍🤝‍🧑 Salespeople Performance", True)

if show_time:
    st.header("Sales Over Time")
    plot_sales_over_time(df)

if show_region:
    st.header("Sales by Region")
    plot_sales_by_country(df)

if show_top:
    st.header("Top Product Sales")
    plot_top_products_pie(df)

if show_country:
    st.header("Sales by Country")
    plot_monthly_income_by_country(df)

if show_comparison:
    st.header("Compare Salesperson Performance")
    compare_salespeople_performance(df)