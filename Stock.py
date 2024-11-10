import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import date, timedelta
# Load stock symbols from symbol.txt
symbol = {}
with open("./symbol.txt") as f:
    for line in f:
        key, val = line.split("|")
        symbol[key] = val.strip()  # Populate the symbol dictionary

st.header("*Stock Portfolio Tracker*")

# Display a dropdown for selecting stocks
stock = st.selectbox('Select the stock you own', symbol.keys())
ticker = symbol[stock]  # Get the ticker code of the selected stock

# Input for the amount of stock owned
amount = st.number_input("Enter the number of shares you own:", min_value=0.0, step=0.01)

# Define date range for the past 7 days
today_date = date.today()
start_date = today_date - timedelta(days=7)

# Fetch stock data for the past 7 days using yfinance
data = yf.download(ticker, start=start_date, end=today_date)

# Display the data if retrieved successfully
if not data.empty:
    # Show only the last 7 days of 'Close' prices
    last_7_days = data.tail(7)
    st.write(f"Displaying data for the past 7 days for {stock} ({ticker})")
    st.line_chart(last_7_days['Close'])

    # Get the most recent closing price
    latest_close_price = last_7_days['Close'].iloc[-1]
    total_value = latest_close_price * amount

    # Display the calculation
    st.write(f"Latest closing price for {stock} ({ticker}): ${latest_close_price:.2f}")
    st.write(f"Total value of your shares: ${total_value:.2f}")
else:
    st.write("No data found for the selected stock.")
