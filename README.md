
# Stock Portfolio Tracker

This is a simple web application built with Streamlit and `yfinance` that allows users to track their stock portfolios. Users can select a stock, enter the number of shares they own, and see the latest market data for their selected stock. If the market is closed (like on Sundays), the application will notify the user that the market is closed.

## Features
- **Stock Selection from `symbol.txt`**: Users can choose stocks from a predefined list in `symbol.txt`.
- **Live Stock Data**: Fetches the latest 7 trading days of closing prices for the selected stock using `yfinance`.
- **Market Closed Notification**: If the application is accessed on a non-trading day (e.g., Sunday), it displays a message informing the user that the market is closed.

## Future Enhancement: Dynamic Symbol Selection
Currently, stock symbols are read from `symbol.txt`. For a dynamic solution, you could modify the code to pull stock symbols programmatically, for example, from an online source like Wikipedia's list of S&P 500 companies. Here’s how you could implement it:

```python
import pandas as pd
import requests

# Function to get S&P 500 symbols dynamically from Wikipedia
def get_sp500_symbols():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url)
    tables = pd.read_html(response.text)
    sp500_df = tables[0]  # The first table on the page is the one we want
    symbols = sp500_df.set_index('Security')['Symbol'].to_dict()  # Dictionary with company name as key and symbol as value
    return symbols

# Use the dynamically fetched symbols instead of loading from symbol.txt
symbol = get_sp500_symbols()
```

By using this approach, you can eliminate the need for `symbol.txt` and have an up-to-date list of symbols for S&P 500 companies. This dynamic solution requires an active internet connection to fetch data from Wikipedia.

## Prerequisites
- **Python 3.x**: Make sure Python 3.x is installed.
- **Dependencies**: The following Python packages are required:
  - `streamlit`: For creating the web interface.
  - `yfinance`: For fetching stock data.
  - `pandas`: For data manipulation.

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install the required packages:
   ```bash
   pip install streamlit yfinance pandas
   ```

3. Make sure you have a `symbol.txt` file with stock symbols. Each line in `symbol.txt` should have the following format:
   ```plaintext
   Company Name|Ticker Symbol
   ```
   Example:
   ```plaintext
   Apple Inc.|AAPL
   Microsoft Corp.|MSFT
   ```

## Usage

1. Run the application:
   ```bash
   streamlit run Stock.py
   ```

2. Open the web application in your browser. Streamlit will display a local URL in the terminal (e.g., `http://localhost:8501`).

3. **Select a Stock**: Choose a stock from the dropdown menu.
4. **Enter Number of Shares**: Input the number of shares you own.
5. **View Data**:
   - If the market is open, the app displays the last 7 days of closing prices for the selected stock along with a line chart.
   - The latest closing price and the total value of your shares (based on the entered amount) are displayed.
   - If it’s a non-trading day (like Sunday), the app shows a message: "Oops, today is Sunday; the market is closed."

## Example of `symbol.txt` File

```plaintext
Apple Inc.|AAPL
Microsoft Corp.|MSFT
Alphabet Inc.|GOOGL
Amazon.com Inc.|AMZN
Tesla Inc.|TSLA
NVIDIA Corp.|NVDA
```

## Troubleshooting

- **No Data Found**: If the application displays "No data found for the selected stock," it may be due to a non-trading day or an issue with the stock symbol. Ensure the stock symbol in `symbol.txt` is correct.
- **Dependencies Not Installed**: Make sure all required packages are installed. Use `pip install -r requirements.txt` if you have a `requirements.txt` file.

## License
This project is open-source and available under the MIT License.
