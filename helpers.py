import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors as pc

def data_cleaning(df):
    '''
    This function cleans the data from the df
    Input/Output
    df = pd.DataFrame
    '''
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_', regex=False)
    df['date'] = pd.to_datetime(df['date'], format='%d-%b-%y') # convert date to datetime
    df['amount'] = df['amount'].replace('[\$,]', '', regex=True).astype(float) #convert amount into float
    return df

def plot_sales_over_time(df):
    """
    This function allows the user to select the aggregation period (Month/Week)
    and plots the sales over time with smooth lines and markers.
    Input:
    df = pd.DataFrame
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

def plot_sales_by_country(df):
    """
    This function generates an interactive bar plot for sales by country or region.
    The user can toggle between sum or average aggregation for sales data.

    Input:
    df = pd.DataFrame
    """

    # Add a selection box to choose the aggregation criteria (e.g., sum or average)
    aggregation_choice = st.selectbox(
        'Choose aggregation method:',
        ['Sum', 'Average']
    )

    # Aggregating data based on user choice
    if aggregation_choice == 'Sum':
        aggregated_df = df.groupby('country', as_index=False)['amount'].sum()
    elif aggregation_choice == 'Average':
        aggregated_df = df.groupby('country', as_index=False)['amount'].mean()

    # Plotly Bar chart for Sales by Country/Region
    fig = px.bar(aggregated_df, x='country', y='amount', title='Sales by Country/Region',
                 color='country', color_continuous_scale='Set2')

    # Optional: format x-axis for better scrolling and rotate x-ticks
    fig.update_layout(
        xaxis_title='Country',
        yaxis_title='Amount',
        xaxis=dict(tickangle=45)
    )

    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

def plot_top_products_pie(df):
    """
    This function allows the user to select how many top products to display in a pie chart
    based on total sales amount.

    Input:
    df = pd.DataFrame
    """

    # Let user pick how many top products to show
    top_n = st.slider('Select number of top products to show:', min_value=3, max_value=15, value=5)

    # Group and sort data
    top_products = df.groupby('product')['amount'].sum().nlargest(top_n).reset_index()

    # Plotly Pie Chart
    fig = px.pie(
        top_products,
        names='product',
        values='amount',
        title=f'Top {top_n} Products by Sales',
        hole=0.3  # For a donut-style chart, optional
    )

    # Show chart
    st.plotly_chart(fig, use_container_width=True)


def plot_monthly_income_by_country(df):
    '''
    This function allows the user to select the countries and visualize
    the sales data for each one.
    df = pd.DataFrame
    '''
    df['month'] = df['date'].dt.to_period('M').dt.to_timestamp()

    available_countries = df['country'].dropna().unique().tolist()
    selected_countries = st.multiselect(
        "Select countries to display:",
        options=sorted(available_countries),
        default=available_countries[:3]
    )

    show_trend = st.checkbox("Add trend line for each country")

    if selected_countries:
        filtered_df = df[df['country'].isin(selected_countries)]

        income_summary = (
            filtered_df.groupby(['month', 'country'], as_index=False)['amount'].sum()
            .rename(columns={'month': 'Month', 'country': 'Country', 'amount': 'Total_Income'})
        )

        # Assign fixed colors from Plotly palette
        color_palette = pc.qualitative.Plotly
        country_colors = {
            country: color_palette[i % len(color_palette)]
            for i, country in enumerate(selected_countries)
        }

        fig = go.Figure()

        for country in selected_countries:
            country_data = income_summary[income_summary['Country'] == country]
            fig.add_trace(go.Scatter(
                x=country_data['Month'],
                y=country_data['Total_Income'],
                mode='lines+markers',
                name=country,
                line=dict(color=country_colors[country], width=2),
                marker=dict(size=6)
            ))

        if show_trend:
            for country in selected_countries:
                country_data = income_summary[income_summary['Country'] == country]
                x_numeric = (country_data['Month'] - country_data['Month'].min()).dt.days
                coeffs = np.polyfit(x_numeric, country_data['Total_Income'], deg=1)
                trend_y = coeffs[0] * x_numeric + coeffs[1]

                # Convert hex to RGBA with opacity
                hex_color = country_colors[country].lstrip('#')
                r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                faded_rgba = f'rgba({r},{g},{b},0.4)'

                fig.add_trace(go.Scatter(
                    x=country_data['Month'],
                    y=trend_y,
                    mode='lines',
                    name=f"{country} Trend",
                    line=dict(color=faded_rgba, width=2, dash='dash'),
                    showlegend=True
                ))

        fig.update_layout(
            title='Monthly Income Trend by Country',
            xaxis_title='Month',
            yaxis_title='Total Income',
            legend_title='Country',
            yaxis_tickprefix='$',
            xaxis=dict(tickangle=45),
            template='plotly_white',
            title_font=dict(size=20),
            legend_font=dict(size=12)
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please select at least one country to display the chart.")


def compare_salespeople_performance(df):
    '''
    This function allows the user to see the salespeople performance
    by country, product or month.
    Input:
    df = pd.DataFrame
    '''
    st.subheader("📊 Compare Salesperson Performance")

    # Select multiple salespeople
    selected_people = st.multiselect("Select Salespeople", sorted(df['sales_person'].unique()), default=df['sales_person'].unique()[:3])
    breakdown = st.radio("Break down by:", ['Country', 'Product', 'Month'])

    if not selected_people:
        st.warning("Please select at least one salesperson.")
        return

    # Filter and group data
    filtered_df = df[df['sales_person'].isin(selected_people)]

    # Dynamic filter based on breakdown
    if breakdown == 'Country':
        # Create a country filter
        country_filter = st.multiselect("Select Countries", sorted(filtered_df['country'].unique()))
        if country_filter:
            filtered_df = filtered_df[filtered_df['country'].isin(country_filter)]
        group_cols = ['sales_person', 'country']
        x_col = 'country'
    elif breakdown == 'Product':
        # Create a product filter
        product_filter = st.multiselect("Select Products", sorted(filtered_df['product'].unique()))
        if product_filter:
            filtered_df = filtered_df[filtered_df['product'].isin(product_filter)]
        group_cols = ['sales_person', 'product']
        x_col = 'product'
    else:  # Month
        # Extract month name from datetime and remove year
        filtered_df['month_name'] = pd.to_datetime(filtered_df['month'], format='%Y-%m').dt.strftime('%B')

        # Define the correct month order
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

        # Create a month filter (only month names, ordered correctly)
        month_filter = st.multiselect("Select Months", sorted(filtered_df['month_name'].unique(), key=lambda x: month_order.index(x)))
        if month_filter:
            filtered_df = filtered_df[filtered_df['month_name'].isin(month_filter)]
        group_cols = ['sales_person', 'month_name']
        x_col = 'month_name'

    # Group and sum sales amount
    grouped = (
        filtered_df
        .groupby(group_cols, as_index=False)['amount']
        .sum()
        .sort_values(by='amount', ascending=False)
    )

    # Plot
    fig = px.bar(grouped, x=x_col, y='amount', color='sales_person', barmode='group',
                 title=f'Sales by {breakdown}',
                 labels={'amount': 'Total Sales'},
                 color_discrete_sequence=px.colors.qualitative.Set2)

    fig.update_layout(
        xaxis_title=breakdown,
        yaxis_title='Sales Amount',
        xaxis_tickangle=45
    )

    st.plotly_chart(fig, use_container_width=True)
