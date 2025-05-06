import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from helpers import *

df = pd.read_csv('sales.csv')
df = data_cleaning(df)
st.title("Analytics Dashboard")

#### plot
# # Create a 'month' column
# df = df.sort_values('date')
# df['month'] = df['date'].dt.to_period('M').dt.to_timestamp()
# # Aggregate by month (sum or mean, depending on what 'amount' represents)
# monthly_df = df.groupby('month', as_index=False)['amount'].sum()


# fig = px.line(monthly_df, x='month', y='amount', title='sales Over Time')
# fig.update_layout(xaxis_title='Date', yaxis_title='Amount')

# # Optional: format x-axis for better scrolling
# fig.update_xaxes(rangeslider_visible=True, tickangle=45)

# st.plotly_chart(fig, use_container_width=True)
# Ensure datetime format and create 'month' column
# Ensure datetime format and create 'month' column


# df['date'] = pd.to_datetime(df['date'])
# df['month'] = df['date'].dt.to_period('M').dt.to_timestamp()

# # Aggregate by month (sum or mean)
# monthly_df = df.groupby('month', as_index=False)['amount'].sum()

# # Plot the smoothed line chart with dots
# fig = px.line(monthly_df, x='month', y='amount', title='Sales Over Time')

# # Smooth the line, add dots at each value, and remove the rangeslider (zoom)
# fig.update_traces(mode='lines+markers', line=dict(shape='spline', smoothing=1.3))

# fig.update_layout(
#     xaxis_title='Month',
#     yaxis_title='Amount',
#     xaxis=dict(tickangle=45)  # Format x-axis
# )

# # Display the plot in Streamlit
# st.plotly_chart(fig, use_container_width=True)

# Streamlit selectbox for week/month selection
aggregation_choice = st.selectbox(
    'Choose aggregation period:',
    ['Month', 'Week']
)
# Aggregating data based on user choice
if aggregation_choice == 'Month':
    df['period'] = df['date'].dt.to_period('M').dt.to_timestamp()
    monthly_df = df.groupby('period', as_index=False)['amount'].sum()
    period_label = 'Month'
elif aggregation_choice == 'Week':
    df['period'] = df['date'].dt.to_period('W').dt.to_timestamp()
    weekly_df = df.groupby('period', as_index=False)['amount'].sum()
    period_label = 'Week'

# Select the appropriate aggregated DataFrame
aggregated_df = monthly_df if aggregation_choice == 'Month' else weekly_df

# Plot the smoothed line chart with dots
fig = px.line(aggregated_df, x='period', y='amount', title=f'Sales Over Time ({period_label})')

# Smooth the line, add dots at each value, and remove the rangeslider (zoom)
fig.update_traces(mode='lines+markers', line=dict(shape='spline', smoothing=1.3))

fig.update_layout(
    xaxis_title=f'{period_label}',
    yaxis_title='Amount',
    xaxis=dict(tickangle=45)  # Format x-axis
)

# Display the plot in Streamlit
st.plotly_chart(fig, use_container_width=True)
