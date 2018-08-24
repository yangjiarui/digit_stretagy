#-*-coding:utf-8-*-
'''

@author:HANDSOME_JERRY
@time:'18-8-2上午10:38'
'''
import json
import requests,time
import urllib
import pandas as pd
dates=pd.date_range('2018-06-30','2018-08-01',freq='D')
dates=dates.values
from coinbase.wallet.client import Client
client = Client('M0110UJ8G2pteyAW', ' wi5cAfH41hG06sVyiYmZ5TQ3EpCKAxN0')
import re
symbol='BTC-USD'
for i in dates:
    i=i.tolist()
    date=re.findall('\d{10}',str(i))[0]
    date=time.localtime(int(date))
    date=time.strftime('%Y-%m-%d',date)
    q=client.get_spot_price(date=date,currency_pair = symbol)
    print("%s Done %s %s"%(date,symbol,q))



#https://api-public.sandbox.pro.coinbase.com//products/BTC-USD/candles
