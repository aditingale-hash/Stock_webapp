import quandl #libraby
import streamlit as st
import pandas as pd
from datetime import date, timedelta
from datetime import date
quandl.ApiConfig.api_key = "_4zc86ZxsiJzYAbrG7xt"   

symbol= {} #creating a dict
today = str(date.today()) # todays date
with open("./symbol.txt") as f:
    for line in f:
        (key, val) = line.split("|")
        symbol[(key)] = val.rstrip()

# opening a symbol file which contains a stcok and code separated by '|'
# readinf through f by line by line
# taking key and vlaue by spliting
# and adding to symbol like this key have this value


st.sidebar.header("*Stock Symbol*")
with st.sidebar.form('Form1'):
  #stock = st.selectbox('wWich stocks you have', symbol.keys())
 # st.form_submit_button('Submit')
 stock = st.sidebar.selectbox(
    'which stocks you have',
   symbol.keys()) # displaing only keys names of stock
ticker = symbol[stock] # getting back the code of stock by stock name
today_1 = date.today()
start = today_1 - timedelta(days=today_1.weekday())
end = start - timedelta(days=6)
data_normal = quandl.get("BSE/"+ticker, start_date=end, end_date=today_1) 
# libraby have this function which takes start and end with code
# data_normal[open] = data_normal[open].astype(float) * 10.00

data = data_normal.T

st.title(f'{stock} portfolio')

st.write(data.loc[:,::-1]) 
int_val = 1
st.sidebar.header("*Enter your Stock*")
with st.sidebar.form(key='my_form'):
  int_val = st.number_input(label= 'How many stocks you have', value=1, step=1)
  submit_button = st.form_submit_button(label='Calculate')
    
st.title('Enter Stock Value of your to check its cureent value')
#display data  now we can disply data like last 5 days so we can plot graph your turn
if(int_val > 1):
  st.title('cureent price of your stock')
  data_normal['Open'] = data_normal['Open'].apply(lambda x: x*int_val)
  data_normal['Close'] = data_normal['Close'].apply(lambda x: x*int_val)
  data_normal['High'] = data_normal['High'].apply(lambda x: x*int_val)
  data_normal['Low'] = data_normal['Low'].apply(lambda x: x*int_val)
  newData = data_normal.T
  # newData = pd.DataFrame(newData,columns=['Open','Close','High', 'Low'])
  st.write(data.loc[:,::-1])
