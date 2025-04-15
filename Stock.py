import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import date, timedelta

# Utility function for caching historical data
@st.cache_data
def get_historical_data(ticker, start, end):
    return yf.download(ticker, start=start, end=end)

st.header("Stock Portfolio Tracker")

# Load stock symbols from symbol.txt
symbol_dict = {}
try:
    with open("./symbol.txt") as f:
        for line in f:
            if "|" in line:
                key, val = line.split("|")
                symbol_dict[key.strip()] = val.strip()  # Populate the symbol dictionary
except Exception as e:
    st.error("Error reading symbol.txt: " + str(e))
    st.stop()

# Dropdown for selecting a stock from the loaded symbols
selected_stock = st.selectbox("Select the stock you own", list(symbol_dict.keys()))
ticker_symbol = symbol_dict[selected_stock]

# Input number of shares owned
num_shares = st.number_input("Enter the number of shares you own", min_value=0, value=0, step=1)

# Update Data button triggers the data fetch process
if st.button("Update Data"):
    # Create a yfinance ticker object
    ticker_obj = yf.Ticker(ticker_symbol)

    # Fetch current price from ticker.info; fall back to the last closing price if needed.
    current_price = None
    try:
        info = ticker_obj.info
        if "regularMarketPrice" in info and info["regularMarketPrice"]:
            current_price = info["regularMarketPrice"]
    except Exception as e:
        st.warning("Unable to fetch market price via ticker.info; attempting fallback. " + str(e))

    if current_price is None:
        try:
            history_data = ticker_obj.history(period="1d")
            if not history_data.empty:
                current_price = history_data["Close"].iloc[-1]
        except Exception as e:
            st.error("Error fetching historical data: " + str(e))

    # Display the current price and portfolio value
    if current_price:
        st.subheader("Current Stock Data")
        st.write(f"**Ticker**: {ticker_symbol}")
        st.write(f"**Current Price**: ${current_price:.2f}")
        if num_shares > 0:
            total_value = current_price * num_shares
            st.write(f"**Total Value of Your Holdings**: ${total_value:.2f}")
    else:
        st.error("Could not retrieve the current price for the selected ticker.")

    # Define the date range for the past 7 days
    today_date = date.today()
    start_date = today_date - timedelta(days=7)

    if today_date.weekday() == 6:  # 6 represents Sunday
        st.warning("Today is Sunday; the market is closed. Displaying the latest available data.")

    # Fetch and display historical closing price data
    data = get_historical_data(ticker_symbol, start_date, today_date)
    if not data.empty and "Close" in data.columns:
        st.subheader("Closing Price Data for the Past 7 Days")
        st.line_chart(data.tail(7)["Close"])
    else:
        st.warning("No historical data available for the selected ticker.")
