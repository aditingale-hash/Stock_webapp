import yfinance as yf
import streamlit as st
import pandas as pd
import requests
from datetime import date, timedelta

# Function to get S&P 500 symbols dynamically from Wikipedia
def get_sp500_symbols():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url)
    tables = pd.read_html(response.text)
    sp500_df = tables[0]  # The first table on the page is the one we want
    symbols = sp500_df['Symbol'].tolist()
    return symbols

# Load symbols dynamically
symbols = get_sp500_symbols()

# Streamlit interface
st.header("*Stock Portfolio Tracker*")

# Dropdown for selecting stocks from the dynamically loaded symbols
stock = st.selectbox('Select the stock you own', symbols)

# Input for the amount of stock owned
amount = st.number_input("Enter the number of shares you own:", min_value=0.0, step=0.01)

# Define date range for the past 7 days
today_date = date.today()
start_date = today_date - timedelta(days=7)

# Fetch stock data for the past 7 trading days using yfinance
data = yf.download(stock, period="7d")

# Display the data if retrieved successfully
if not data.empty:
    # Show only the last 7 trading days of 'Close' prices as a line chart
    last_7_days = data.tail(7)
    st.write(f"Displaying closing price data for the past 7 trading days for {stock}")
    st.line_chart(last_7_days['Close'])

    # Get the most recent closing price
    latest_close_price = last_7_days['Close'].iloc[-1]
    st.write(f"Latest closing price for {stock}: ${latest_close_price:.2f}")

    # Display total value only if the user has entered an amount
    if amount > 0:
        total_value = latest_close_price * amount
        st.write(f"**Total value of your shares:** ${total_value:.2f}")

else:
    st.write("No data found for the selected stock.")
