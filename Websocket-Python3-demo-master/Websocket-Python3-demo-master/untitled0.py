# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 14:18:03 2018

@author: qzd123
"""

import matplotlib.pyplot as plt
import numpy as np
import requests
import urllib.parse
import urllib.request
import urllib
# params  CategoryId=808 CategoryType=SiteHome ItemListActionName=PostList PageIndex=3 ParentCategoryId=0 TotalPostCount=4000

user_agent='Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
headers = {'User-Agent':user_agent}
data = urllib.parse.urlencode(values)
response_result = urllib.request.urlopen('https://www.huobi.com/zh-cn/').read()
html = response_result.decode('utf-8')



