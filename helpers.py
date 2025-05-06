import pandas as pd
import streamlit as st
import plotly.express as px

def data_cleaning(df):
    '''
    This function cleans the data from the df
    Input/Output
    df = pd.Data Frame
    '''
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_', regex=False)
    df['date'] = pd.to_datetime(df['date'], format='%d-%b-%y') # convert date to datetime
    df['amount'] = df['amount'].replace('[\$,]', '', regex=True).astype(float) #convert amount into float
    return df

def plot_sales_over_time(df):
    """
    This function allows the user to select the aggregation period (Month/Week)
    and plots the sales over time with smooth lines and markers.
    """

    # Streamlit selectbox for week/month selection
    aggregation_choice = st.selectbox(
        'Choose aggregation period:',
        ['Month', 'Week']
    )

    # Aggregating data based on user choice
    if aggregation_choice == 'Month':
        df['period'] = df['date'].dt.to_period('M').dt.to_timestamp()
        aggregated_df = df.groupby('period', as_index=False)['amount'].sum()
        period_label = 'Month'
    elif aggregation_choice == 'Week':
        df['period'] = df['date'].dt.to_period('W').dt.to_timestamp()
        aggregated_df = df.groupby('period', as_index=False)['amount'].sum()
        period_label = 'Week'

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