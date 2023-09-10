import streamlit as st
import pandas as pd


# Load CSV data into pandas DataFrames
df_portfolio = pd.read_csv("protfolio.csv")
df_price = st.session_state['df']

# Create a Streamlit app
st.title("Portfolio Overview")

# Get unique portfolios from the DataFrame
portfolios = df_portfolio['Portfolio'].unique()

# Iterate through each portfolio and display its aggregated data
for portfolio in portfolios:
    st.subheader(f"Portfolio: {portfolio}")
    
    # Filter data for the current portfolio
    portfolio_data = df_portfolio[df_portfolio['Portfolio'] == portfolio]


    st.write(portfolio_data['Buy Value'])


    info = {}

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
    
    # Calculate the total portfolio value for the current portfolio
    portfolio_value = merged_df['Current Value'].sum()
    
    # Calculate the difference between buying value and current value for each coin
    merged_df['Difference'] = (merged_df['Current Value'] - 
                                (merged_df['Buy Value']))
    
    portfolio_diff = merged_df['Difference'].sum()

    # Display the aggregated data as a table for the current portfolio
    st.write(f"Portfolio: {portfolio}")
    st.write(merged_df)
    
    # Display a bar chart showing the current value of each coin for the current portfolio
    st.bar_chart(merged_df[['Name', 'Current Value']].set_index('Name'))
    
    # Display the total portfolio value for the current portfolio
    st.write(f"Total Portfolio Value: ${portfolio_value:.2f} (${portfolio_diff:.2f})")

