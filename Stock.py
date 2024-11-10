import yfinance as yf
import streamlit as st
import pandas as pd

# Function to dynamically fetch S&P 500 symbols
def get_sp500_symbols():
    sp500_ticker = yf.Ticker("^GSPC")  # S&P 500 Index ticker
    sp500_symbols = [ticker for ticker in sp500_ticker.history(period="1d").columns]
    return sp500_symbols

st.header("*Stock Portfolio Tracker*")

# Dynamically get the list of S&P 500 symbols
symbols = get_sp500_symbols()

# Allow the user to select from the dynamically fetched symbols
stock = st.selectbox('Select the stock you own', symbols)
ticker = stock  # Directly use the selected stock symbol

# Input for the amount of stock owned
amount = st.number_input("Enter the number of shares you own:", min_value=0.0, step=0.01)

# Fetch stock data for the last 7 trading days using yfinance
data = yf.download(ticker, period="7d")  # Use period to get last 7 trading days

# Display the data if retrieved successfully
if not data.empty:
    # Show only the last 7 trading days of 'Close' prices as a line chart
    last_7_days = data.tail(7)
    st.write(f"Displaying closing price data for the past 7 trading days for {stock} ({ticker})")
    st.line_chart(last_7_days['Close'])

    # Get the most recent closing price
    latest_close_price = last_7_days['Close'].iloc[-1]
    st.write(f"Latest closing price for {stock} ({ticker}): ${latest_close_price:.2f}")

    # Display total value only if the user has entered an amount
    if amount > 0:
        total_value = latest_close_price * amount
        st.write(f"**Total value of your shares:** ${total_value:.2f}")

else:
    st.write("No data found for the selected stock.")
