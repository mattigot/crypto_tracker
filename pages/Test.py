import streamlit as st
import pandas as pd
import plotly.express as px 
from common.price_metric import *

df = st.session_state['df']
# Load CSV data into pandas DataFrames
df_portfolio = pd.read_csv("protfolio.csv")
df_price = st.session_state['df']

# Create a Streamlit app
st.title("Portfolio Overview")

# Get unique portfolios from the DataFrame
portfolios = df_portfolio['Portfolio'].unique()

info = {}
info2 = {}
for portfolio in portfolios:
    info[portfolio] = {}
    info2[portfolio] = {}

# Iterate through each portfolio and display its aggregated data
for portfolio in portfolios:
    # Filter data for the current portfolio
    portfolio_data = df_portfolio[df_portfolio['Portfolio'] == portfolio]

    # Create agg_df by aggregating data based on "Ticker" for the current portfolio
    agg_df = portfolio_data.groupby('Ticker').agg({
        'Name': 'first',
        'Exchange': 'first',
        'Units': 'sum',
        'Buy Value': 'sum',
        'Buy Percent': 'sum',
    }).reset_index()
    
    # Merge agg_df with price data using "Ticker"
    merged_df = pd.merge(agg_df, df_price, on='Ticker')
    
    # Calculate the current value of each coin
    merged_df['Current Value'] = merged_df['Units'] * merged_df['price']
   
    # Calculate the difference between buying value and current value for each coin
    merged_df['Difference'] = (merged_df['Current Value'] - 
                                (merged_df['Buy Value']))
    info[portfolio]['merged_df'] = merged_df

    # Calculate the total portfolio value and dif for the current portfolio
    info2[portfolio]['value'] = merged_df['Current Value'].sum()
    info2[portfolio]['buy_value'] = merged_df['Buy Value'].sum()
    info2[portfolio]['diff'] = merged_df['Difference'].sum()
    info2[portfolio]['diff_%'] = 100 * ((info2[portfolio]['value'] / info2[portfolio]['buy_value']) - 1)


df_gen = pd.DataFrame.from_dict(info2, orient='index')

display_coin_container2(df_gen)
# Summarize portfolio info in a table
container = st.container()
col1, col2 = container.columns(2, gap = "small")

fig_value = px.pie(df_gen, values='value', names=df_gen.index, title='Portfolio Allocation')
#fig_loser = px.pie(df_gen, values='loser', names=df_gen.index, title='Portfolio Losers')

#fig_gainer = px.pie(df_gen, values='loser', names=df_gen.index, title='Portfolio Gainers')

st.table(df_gen)


with col1: 
    st.plotly_chart(fig_value)

with col2:
    #st.plotly_chart(fig_loser)
    info_df = pd.DataFrame.from_dict(info2, orient='index')
    st.bar_chart(info_df['diff'])

    #st.plotly_chart(fig_gainer)

# Iterate through each portfolio and display its aggregated data
for portfolio in portfolios:
    st.subheader(f"Portfolio: {portfolio}")

    merge_df_l = info[portfolio]['merged_df']
    portfolio_value = info2[portfolio]['value']
    portfolio_diff = info2[portfolio]['diff']

    # Display the aggregated data as a table for the current portfolio
    st.write(f"Portfolio: {portfolio}")
    st.write(merge_df_l)
    
    # Display a bar chart showing the current value of each coin for the current portfolio
    #st.pie(merged_df[['Name', 'Current Value']].set_index('Name'))
    fig = px.pie(merge_df_l, values='Current Value', names='Name', title='Portfolio Current Value')
    st.plotly_chart(fig)
    # Display the total portfolio value for the current portfolio
    st.write(f"Total Portfolio Value: ${portfolio_value:.2f} (${portfolio_diff:.2f})")
