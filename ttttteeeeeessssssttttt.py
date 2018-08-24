# encoding: utf-8
'''
@author: headsome jerry
@time:18-8-5下午1:11
@file_name:ttttteeeeeessssssttttt.py.py
'''

from pandas_datareader import data as pdr
import pandas as pd
import fix_yahoo_finance as yf
yf.pdr_override() # <== that's all it takes :-)
bits=pdr.get_iex_symbols()[8658:]
import quandl
# download dataframe
#data = pdr.get_data_yahoo("SPY", start="2010-01-01", end="2017-04-30")
#data2=pdr.get_data_yahoo('AAPL',start="2010-01-01", end="2017-04-30")
# writer=pd.ExcelWriter('fulll.xlsx')
# data.to_excel(writer,'1')
# data2.to_excel(writer,'2')
# writer.save()
# pdr.get_data_yahoo("XLM",start="2010-01-01", end="2017-04-30")

quandl.ApiConfig.api_key = 'vNbJmE3vy2XtEHpAVyWT'

q=quandl.get('GDAX/ETH_EUR')

qq=quandl.get('BCHARTS/BITFLYERUSD', start_date='2016-08-04', end_date='2018-08-04')