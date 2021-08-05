import quandl #libraby
import streamlit as st
import pandas as pd
from datetime import date, timedelta
from datetime import date
quandl.ApiConfig.api_key = "_4zc86ZxsiJzYAbrG7xt"

symbol= {} #creating a dict
today = str(date.today()) # todays date
with open("C:/Users/aditi/PycharmProjects/pythonProject/symbols.txt") as f:
    for line in f:
        (key, val) = line.split("|")
        symbol[(key)] = val.rstrip()

# opening a symbol file which contains a stcok and code separated by '|'
# readinf through f by line by line
# taking key and vlaue by spliting
# and adding to symbol like this key have this value


st.sidebar.header("**stock Symbol**")
stock = st.sidebar.selectbox(
    'which stocks you have',
  symbol.keys()) # displaing only keys names of stock
ticker = symbol[stock] # getting back the code of stock by stock name
today_1 = date.today()
start = today_1 - timedelta(days=today_1.weekday())
end = start - timedelta(days=6)
data_normal = quandl.get("BSE/"+ticker, start_date=end, end_date=today_1) # libraby have this function which takes start and end with code
data = data_normal.T

st.title(f'{stock} portfolio')
st.write(data.loc[:,::-1]) #display data  now we can disply data like last 5 days so we can plot graph your turn
open = data_normal['Open']
close = data_normal['Close']
Low = data_normal['Low']
High = data_normal['High']
bar_grpah_disply_open_Close = pd.DataFrame(data_normal,columns=['Open', 'Close', 'Low', 'High'])
st.bar_chart(bar_grpah_disply_open_Close)