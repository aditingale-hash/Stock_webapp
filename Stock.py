import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import date, timedelta

# --- Utility Function for Caching (Streamlit 1.18+ uses @st.cache_data) ---
@st.cache_data
def get_historical_data(ticker, start, end):
    return yf.download(ticker, start=start, end=end)

st.header("Stock Portfolio Tracker")

# --- Load Symbols ---
symbol_dict = {}
try:
    with open("./symbol.txt") as f:
        for line in f:
            # Expect each line in format: "Stock Name|Ticker"
            if "|" in line:
                key, val = line.split("|")
                symbol_dict[key.strip()] = val.strip()
except Exception as e:
    st.error("Error reading symbol.txt: " + str(e))

# --- Stock Entry Option ---
entry_option = st.radio("Choose how to enter your stock", ("Select from list", "Enter ticker manually"))

if entry_option == "Select from list":
    if symbol_dict:
        stock_name = st.selectbox("Select the stock you own", list(symbol_dict.keys()))
        ticker_symbol = symbol_dict[stock_name]
    else:
        st.error("No symbols available in symbol.txt")
        st.stop()
else:
    ticker_symbol = st.text_input("Enter the stock ticker (e.g., AAPL)").upper().strip()
    if not ticker_symbol:
        st.info("Please enter a valid ticker symbol.")
        st.stop()

# --- Input number of shares ---
num_shares = st.number_input("Enter the number of shares you own", min_value=0, value=0, step=1)

# --- Fetch Current Price ---
# Attempt to retrieve current market price using yfinance's info dictionary;
# fallback to the latest closing price using history() if necessary.
ticker_obj = yf.Ticker(ticker_symbol)
current_price = None
try:
    info = ticker_obj.info
    if "regularMarketPrice" in info and info["regularMarketPrice"]:
        current_price = info["regularMarketPrice"]
except Exception as e:
    st.warning("Unable to fetch market price using ticker.info; attempting fallback. " + str(e))

if current_price is None:
    # Fallback: Get the last closing price from the most recent trading day
    try:
        history_data = ticker_obj.history(period="1d")
        if not history_data.empty:
            current_price = history_data["Close"].iloc[-1]
    except Exception as e:
        st.error("Error fetching historical data: " + str(e))

# --- Display Current Price and Portfolio Value ---
if current_price:
    st.subheader("Current Stock Data")
    st.write(f"**Ticker**: {ticker_symbol}")
    st.write(f"**Current Price**: ${current_price:.2f}")
    if num_shares > 0:
        total_value = current_price * num_shares
        st.write(f"**Total Value of Your Holdings**: ${total_value:.2f}")
else:
    st.error("Could not retrieve the current price for the given ticker.")

# --- Chart the Past 7 Days of Closing Prices ---
today_date = date.today()
start_date = today_date - timedelta(days=7)

# Note: Even if today is a market closed day, this call retrieves the last available trading data.
if today_date.weekday() == 6:  # Sunday check
    st.warning("Market is closed today (Sunday). Displaying the latest available data.")

data = get_historical_data(ticker_symbol, start_date, today_date)
if not data.empty and "Close" in data.columns:
    st.subheader("Closing Price Data for the Past 7 Days")
    last_7_days = data.tail(7)
    st.line_chart(last_7_days["Close"])
else:
    st.warning("No historical data available for the selected ticker.")
