import yfinance as yf  # Updated library for stock data
import streamlit as st
import pandas as pd
from datetime import date, timedelta

# Load stock symbols from symbol.txt
symbol = {}  # Create a dictionary for stock symbols
today = str(date.today())  # Get today's date as a string
with open("./symbol.txt") as f:
    for line in f:
        key, val = line.split("|")
        symbol[key] = val.strip()  # Populate the symbol dictionary

st.header("*Stock Symbol*")

# Display a dropdown for selecting stocks
stock = st.selectbox('Which stocks you have', symbol.keys())
ticker = symbol[stock]  # Get the ticker code of the selected stock

# Define date range for data retrieval
today_date = date.today()
start_date = today_date - timedelta(days=today_date.weekday())  # Start of the week
end_date = start_date - timedelta(days=6)  # One week back

# Fetch stock data using yfinance
data_normal = yf.download(ticker, start=str(end_date), end=str(today_date))

# Display the data if retrieved successfully
if not data_normal.empty:
    st.write(f"Displaying data for {stock} ({ticker})")
    st.line_chart(data_normal['Close'])  # Display the closing price
else:
    st.write("No data found for the selected stock.")
