# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import json,time,sys,re
import pandas as pd
sys.path.append('/home/jerry/inteligient/bitbucket/bitcoin/rest-master/rest-master')
sys.path.append('/home/jerry/inteligient/bitbucket/bitcoin/REST-Python3-demo-master')
import HuobiServices as huobi
#import Client as okcoin
#import more_data as binance
import re
import matplotlib.pyplot as plt
#plt.ion()
#plt.figure(2)
huo,ok=[],[]
def stifttime(x):
    Serise=pd.Series(x)
    cur = int(re.findall('\d{10}', str(x['id']))[0])
    timit = time.localtime(cur)
    tim = time.strftime("%Y-%m-%d %H:%M:%S", timit)
    Serise[Serise.index == 'id'] =tim
    return  Serise
def process_symbols(input,ouput):
    if ouput == 'huobi':
        return str(input).lower()
    elif ouput == 'binance':
        return str(input).upper()

if __name__ == '__main__':
    we=huobi.get_symbols()
    dddd=huobi.get_kline('etcusdt','1min')
#    binance_client=binance.client
    ticks=pd.DataFrame(columns=['id', 'open', 'close', 'low', 'high', 'amount', 'vol', 'count'])
    while 1:
        try:
            cur=dddd['data'].pop(0)
            ticks=ticks.append(stifttime(cur),ignore_index=True)
        except:
            print('分钟数据处理完成')
            break

    print('起始 %s 与 结束 %s:'%(ticks['id'].values[0],ticks['id'].values[-1]))
    all_name = []
    for i in we['data']:
        #print(i['symbol'])
        all_name.append(i['symbol'])
import os
if os.path.exists('/media/jerry/JERRY/ticks_data/' + str(time.strftime("%Y-%m-%d", time.localtime()))):
    pass
else:
    os.makedirs('/media/jerry/JERRY/ticks_data/' + str(time.strftime("%Y-%m-%d", time.localtime())))

def current_symbol(pair_name):
    global binance_client
    k=0
    f = pd.DataFrame(columns=['open', 'low', 'close', 'high', 'time', 'vol'])
    #x1,x2='btc','usd'
    os.chdir('/media/jerry/JERRY/ticks_data/' + str(time.strftime("%Y-%m-%d", time.localtime())))
    while 1:
        k+=1

        time.sleep(0.5)
        q=huobi.get_ticker(process_symbols(pair_name,'huobi'))
#        binance=binance_client.get_symbol_ticker()
#        binance=pd.DataFrame(binance)
        #binance.index=binance.iloc[:,0]
        #binance=binance.iloc[:,0]
        #print(binance[binance['symbol']==process_symbols(pair_name,'binance')])
#        binance=
        #print(len(q))
        cur=int(re.findall('\d{10}',str(q['ts']))[0])
        timit=time.localtime(cur)
        tim=time.strftime("%Y-%m-%d %H:%M:%S", timit)
        data=q['tick']
        hh=pd.Series([data['open'],data['low'],data['close'],data['high'],tim,data['vol']],index=['open','low','close','high','time','vol'])
        f=f.append(hh,ignore_index=True)
        
        #print('Done %s %s'%(tim,data['close']))
        # try:
        #     qq=okcoin.okcoinSpot.ticker(x1+'_'+x2)
        # except:
        #     qq=None
#        binance=binance[binance['symbol'] == process_symbols(pair_name, 'binance')]['price'].values[0]
    #####print('%s huobi:%s binance:%s symbol:%s'%(tim,data['close'],None,pair_name))

        if k==10:
            f.index = pd.DatetimeIndex(f.iloc[:, 4])
            f = f.drop('time', axis=1)
            f = f.resample('3s', 'mean')
            with open('%s.txt'%pair_name,'a') as file:
                file.writelines(str(f.columns.values.tolist())+'\n')
                for i in range(f.shape[0]):
                    c=f.iloc[i,:].values.tolist()
                    file.writelines(str(c.append(f.iloc[i,:].name.strftime('%Y-%m-%d %H:%M:%S')))+'\n')

            print('%s huobi:%6.6f symbol:%8s' % (tim, data['close'],pair_name))
            f = pd.DataFrame(columns=['open', 'low', 'close', 'high', 'time', 'vol'])
 #           print(f)
        #huo.append(data['close'])
#        ok.append(qq['ticker']['buy'])
        ##plt.plot(huo)
        #plt.subplot(212)
        #plt.plot(ok)
        #plt.draw()
        c_tim1=time.strftime("%X",time.localtime())
        c_tim2=time.strftime("%x", time.localtime())
        if  c_tim2=='08/18/18' and c_tim1>='03:30:00' :
            #f.index=pd.DatetimeIndex(f.iloc[:,4])
            #f=f.drop('time',axis=1)
            #f=f.resample('3s','mean')
            break
        #f.to_csv('/home/jerry/PycharmProjects/blochain/ticks_data/%s.csv'%pair_name)
    return f,pair_name
qq=current_symbol(all_name[4])
import multiprocessing,os
#
# pools=multiprocessing.Pool(processes=120)
# result=[]
# for j in range(len(all_name)):
#     result.append(pools.apply_async(current_symbol,args=(all_name[j],)))
# pools.close()
# pools.join()

print('all_done')
#full=pd.DataFrame(columns=['open', 'low', 'close', 'high', 'vol'])
# if os.path.exists('/home/jerry/PycharmProjects/blochain/ticks_data/' + str(time.strftime("%Y-%m-%d", time.localtime()))):
#     pass
# else:
#     os.makedirs('/home/jerry/PycharmProjects/blochain/ticks_data/' + str(time.strftime("%Y-%m-%d", time.localtime())))
# for cur in result:
#     try:
#         con,name=cur.get()
#         if len(con)==1:
#             print('Drop:%s'%name)
#         else:
#             con.to_csv('/home/jerry/PycharmProjects/blochain/ticks_data/%s/%s.csv'%(str(time.strftime("%Y-%m-%d", time.localtime())),name))
#     except:
#         print('unknown error')
#current_symbol('BTCUSDT')
#qq=current_symbol(all_name[2])
#print (q)

#print('比较')
#


