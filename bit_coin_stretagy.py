# -*- coding: utf-8 -*-
#作者: handsome_jerry
#时间:18-8-24下午2:57
#文件:bit_coin_stretagy.py


import tushare as ts
import pandas as pd
import numpy as np
import datetime as da
import json,time,sys,re
# import pandas as pd
# sys.path.append('/home/jerry/inteligient/bitbucket/bitcoin/rest-master/rest-master')
sys.path.append('/home/jerry/inteligient/git_version/bitbucket/bitcoin/REST-Python3-demo-master')
import HuobiServices as huobi_py
import time


def signal(code,input_tick):
    start = 0
    ind = 0
    input_tick=np.round(input_tick,4)
    # print('相关价格指标:',input_tick)
    b = 0
    while 1:
        #        time.sleep(0.85)
        a = b
        start += 1
        # tick = ts.get_realtime_quotes(code)
        tick = huobi_py.get_ticker(code)
        tick['tick']['current_time'] = tick['ts']
        tick = stifttime(tick['tick'])
        b = tick['current_time']
        if a != b:
            ti_ck = tick
            if float(ti_ck['close']) > input_tick:
                ind += 1
            elif float(ti_ck['close']) == input_tick:
                ind += 0
            else:
                ind += -1
        if start == 10:
            break
        if ind >= 1:
            return 1, 'upper(next_tick_would_be_lower)', float(ti_ck['close']), ti_ck['current_time'],ti_ck['amount']
        elif ind == 0:
            return 1, 'same', float(ti_ck['close']), ti_ck['current_time'],float(ti_ck['amount'])
        else:
            return -1, 'lower(next_tick_would_be_upper)', float(ti_ck['close']), ti_ck['current_time'],float(ti_ck['amount'])


codes = ts.get_stock_basics()
import time
import requests

def stifttime(x):
    Serise=pd.Series(x)
    cur = int(re.findall('\d{10}', str(Serise['current_time']))[0])
    timit = time.localtime(cur)
    tim = time.strftime("%Y-%m-%d %H:%M:%S", timit)
    Serise[Serise.index == 'current_time'] =tim
    return  Serise

def Main(start, codes,daynight):

    k = 1
    for code, name in zip(codes[start:start + 1], codes[start:start + 1]):
        # writer=pd.ExcelWriter('F:\\share\\stocks\\all_a_stocks.xlsx')
 #time       # now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # if now <= time.strftime('%Y-%m-%d 09:30:00', time.localtime()) or (now >= time.strftime('%Y-%m-%d 11:34:00',
        #                                                                                         time.localtime()) and
        #         now <= time.strftime('%Y-%m-%d 13:00:00', time.localtime())) or now >= time.strftime('%Y-%m-%d 15:05:00',
        #                                                                                             time.localtime()):
        #     print('当前时间还没有进行交易')
        #     break
        k += 1
        #    print('%.2f%% has Done\n'%(np.round(k/len(codes[1]),4)*100))
        q1 = 0

        w1, w2 = 0, 0
        try:
            price = []
            prob = []
            nod=[]
            sure_to_up=[]
            while 1:
                q2 = q1
                c1 = w1
                c2 = w2
                # tick = ts.get_realtime_quotes(code)
                tick = huobi_py.get_ticker(code)
                tick['tick']['current_time'] = tick['ts']
                tick=stifttime(tick['tick'])
                q1 = tick['current_time']  ## == da.datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
                if q1 != q2:
                    tick_data = tick
                    price.append((tick['current_time'] , float(tick_data['close']),float(tick_data['amount'])))
                else:
                    continue
                # time.sleep(5)
                #            print(price)
                #             q=w.wsi(str(code),"open,high,close,low,amt","2018-08-19 09:00:00",datetime.now())
                time_bs = (da.datetime.strptime(tick['current_time'],
                                                '%Y-%m-%d %H:%M:%S') + da.timedelta(minutes=1)).strftime(
                    '%Y-%m-%d %H:%M:00')
                time_bs = da.datetime.strptime(time_bs, '%Y-%m-%d %H:%M:%S')

                if da.datetime.now().strftime('%Y-%m-%d %H:%M:%S') >= (time_bs - da.timedelta(seconds=3)).strftime(
                        '%Y-%m-%d %H:%M:%S') and da.datetime.now().strftime('%Y-%m-%d %H:%M:%S') <= (
                        time_bs + da.timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S'):
                    #            if np.isnan(np.sum(q.Data[0][4])):
                    #                print('%s is all nan'%name)
                    #                continue
                    hist = huobi_py.get_kline('etcusdt', '1day')

                    # hist = ts.get_k_data(code, ktype='D', start='2018-08-06', end='2018-08-21')
                    print('整分钟信号(以之前5天收盘价均值为指标)')
                    res, _, close, tim ,amt= signal(code,np.mean([i['close'] for i in hist['data'][:5]]))
                    print('%s: price:%.4f time:%s  should:%s' % (name, close, tim, _))
                    prob = prob[5:]
                    mun=(1-np.round(np.sum(prob) / len(prob), 4)) * 100
                    if np.isnan(mun):
                        print('%s此时还没有数据(由于移动平均窗口为%d)'%(name,4))
                    else:
                        try:
                            print('%s当前分钟内上涨次数统计概率为: %.2f%% 当前分钟内总趋势为上涨或持平的置信度为: %.2f%%' % (name,mun,(np.round(np.sum(nod)/len(nod),4))*100))
                        except:
                            print('%s上分钟内没有有效价格(backend by amont)'%name)
                    prob ,nod ,sure_to_up= [],[],[]

                    print('\n')
                #                price.append(res*close)
                else:
                    cur = pd.Series(list(map(lambda x: x[1], price))).rolling(5).mean()
                    res, _, close, tim ,amt= signal(code,cur.values[-1])
                    w1 = tim
                    if w1 != c1:
                        prob.append(res)
                        print('%s: price:%.4f time:%s  should:%s' % (name, close, tim, _))
                        xxx = list(map(lambda x: x[2], price))
                        vol = pd.Series(xxx)
                        vol=vol.sort_index(ascending=False)
                        vol = (vol / vol.shift(1)) - 1
                        if vol.values[-1] >= vol[:-1].describe()['75%']:
                            print('当前成交量统计显著的支持了当前tick级别(左侧指标)的预测，大概率开启日内短时趋势形态')
                            nod.append(res)

                            for i in range(len(nod),0,-1):
                                try:
                                    cur=np.sum(nod[i-6:i])
                                    if cur==6:
                                        # print(55*'^_^')
                                        if i>=0.5*len(nod):
                                            print(20*'<'+'强上涨信号'+24*'>')
                                        break
                                    elif cur==-4:
                                        if i >= 0.5 * len(nod):
                                            print(20*'<'+'强下跌信号'+24*'>')
                                        # hh=i
                                        break

                                except:
                                    continue



                        elif vol.values[-1] <= vol[:-1].describe()['25%']:
                            # print('当前tick价格指标没有交易支撑，小概率延续当前趋势')
                            pass
                        else:
                            pass
                    # except:
                    #     res, _, close, tim = signal(code, cur.values[0])
                    #     prob.append(res)
                    #     prob = prob[5:]
                    #     # w1 = tim
                    #     # if w1 != c1:
                    #     print('%s: price:%.4f time:%s  should:%s' % (name, close, tim, _))
                    if daynight=='am':
                        if price[-1][0] >= time.strftime('%Y-%m-%d 11:30:00', time.localtime()):
                            break
                    if daynight=='pm':
                        if price[-1][0] >= time.strftime('%Y-%m-%d 24:01:00', time.localtime()):
                            break
            # df=pocess_stock(q)
            #        with open('E:\\stocks_ticks_data\\'+str(name)+'.txt','a') as f:
            #            f.writelines('open,high,close,low,amt,time'+'\n')
            #            for i in range(df.shape[0]):
            #                cur=df.iloc[i,:]
            #                line,tim=cur.values.tolist(),cur.name
            #                line.append(tim)
            #                f.writelines(str(line)+'\n')
            #print('%s has writing Done and shape is %s' % (name, df.shape))

        except ZeroDivisionError as e:
            print('error', e)
        except requests.exceptions.ReadTimeout as e:
            print('error api needs rest')
    # writer.save()


#
names=huobi_py.get_symbols()
names=[i['symbol'] for i in names['data']]
Main(5, names,daynight='pm')

# import multiprocessing
# pools=multiprocessing.Pool(processes=150)
# res=[]
# for i in range(len(codes)):
#    res.append(pools.apply_async(Main,(i,codes,'pm')))
# pools.close()
# pools.join()
#

