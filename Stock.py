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
    st.stop()

# Ensure at least one symbol is available
if not symbol_dict:
    st.error("No symbols available in symbol.txt")
    st.stop()

# --- Stock Selection (Dropdown Only) ---
# By default, the first available stock is selected.
stock_names = list(symbol_dict.keys())
stock_name = st.selectbox("Select the stock you own", stock_names, index=0)
ticker_symbol = symbol_dict[stock_name]

# --- Input number of shares ---
num_shares_input = st.number_input("Enter the number of shares you own", min_value=0, value=0, step=1)

# --- Session State to Control When Data Updates ---
# On first load, store the default selection in session state.
if "ticker_to_use" not in st.session_state:
    st.session_state.ticker_to_use = ticker_symbol
if "shares_to_use" not in st.session_state:
    st.session_state.shares_to_use = num_shares_input

# The 'Enter' button will update these values.
if st.button("Enter"):
    st.session_state.ticker_to_use = ticker_symbol
    st.session_state.shares_to_use = num_shares_input

# Use the stored values to determine what data to display.
ticker_used = st.session_state.ticker_to_use
shares_used = st.session_state.shares_to_use

# --- Fetch Current Price ---
ticker_obj = yf.Ticker(ticker_used)
current_price = None
try:
    info = ticker_obj.info
    if "regularMarketPrice" in info and info["regularMarketPrice"]:
        current_price = info["regularMarketPrice"]
except Exception as e:
    st.warning("Unable to fetch market price using ticker.info; attempting fallback. " + str(e))

if current_price is None:
    try:
        history_data = ticker_obj.history(period="1d")
        if not history_data.empty:
            current_price = history_data["Close"].iloc[-1]
    except Exception as e:
        st.error("Error fetching historical data: " + str(e))

# --- Display Current Price and Portfolio Value ---
if current_price:
    st.subheader("Current Stock Data")
    st.write(f"**Ticker**: {ticker_used}")
    st.write(f"**Current Price**: ${current_price:.2f}")
    if shares_used > 0:
        total_value = current_price * shares_used
        st.write(f"**Total Value of Your Holdings**: ${total_value:.2f}")
else:
    st.error("Could not retrieve the current price for the selected ticker.")

# --- Chart the Past 7 Days of Closing Prices ---
today_date = date.today()
start_date = today_date - timedelta(days=7)
if today_date.weekday() == 6:  # Sunday check
    st.warning("Market is closed today (Sunday). Displaying the latest available data.")

data = get_historical_data(ticker_used, start_date, today_date)
if not data.empty and "Close" in data.columns:
    st.subheader("Closing Price Data for the Past 7 Days")
    last_7_days = data.tail(7)
    st.line_chart(last_7_days["Close"])
else:
    st.warning("No historical data available for the selected ticker.")
