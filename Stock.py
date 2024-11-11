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


# Define date range for the past 7 days
today_date = date.today()
start_date = today_date - timedelta(days=7)

# Check if today is Sunday
if today_date.weekday() == 6:  # 6 represents Sunday
    st.warning("Oops, today is Sunday; the market is closed.")
else:
    # Fetch stock data for the past 7 days using yfinance
    data = yf.download(ticker, start=start_date, end=today_date)

    # Check if data is available and contains the 'Close' column
    if not data.empty and 'Close' in data.columns:
        # Show only the last 7 days of 'Close' prices as a line chart
        last_7_days = data.tail(7)
        st.write(f"Displaying closing price data for the past 7 days for {stock}")
        st.line_chart(last_7_days['Close'])
