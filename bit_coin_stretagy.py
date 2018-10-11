# -*- coding: utf-8 -*-
#作者: handsome_jerry
#时间:18-8-24下午2:57
#文件:bit_coin_stretagy.py


# import tushare as ts
import pandas as pd
import numpy as np
import datetime as da
import json,time,sys,re
import multiprocessing
# import pandas as pd
# sys.path.append('/home/jerry/inteligient/bitbucket/bitcoin/rest-master/rest-master')
sys.path.append('/media/jerry/DATA/jerry_git/git_version_control/digit_stretagy/REST-Python3-demo-master')
import HuobiServices as huobi_py
import time
# import numpy as np

def depth_main(num_str):
    q=huobi_py.get_depth(num_str.split(' ')[0], num_str.split(' ')[1])
    bids=[i[0]*i[1] for i in q['tick']['bids']]
    asks=[i[0]*i[1] for i in q['tick']['asks']]
    return (float(np.sum(bids) - np.sum(asks)), 1.0 * (np.sum(bids) - np.sum(asks)) / np.sum(np.sum(bids) + np.sum(asks)))


def pocess_depth(code):
    # global code
    pools = multiprocessing.Pool(processes=6)
    q=['step0', 'step1', 'step2', 'step3', 'step4', 'step5']
    q=[str(code)+' '+i for i in q]
    res=pools.map(depth_main,q)
    pools.close()
    pools.join()
    return res


def get_current_close(code):
    try:
        r=(huobi_py.get_ticker(code)['tick']['close'],code)
    except:
        r=None
    return r



def signal(code,input_tick):
    start = 0
    ind = 0
    liq=0
    input_tick=np.round(input_tick,4)
    # print('相关价格指标:',input_tick)
    b = 0
    while 1:
        #        time.sleep(0.85)
        a = b
        start += 1
        # tick = ts.get_realtime_quotes(code)
        tick = huobi_py.get_ticker(code)
        # depth = pocess_depth(code)
        try:
            depth = pocess_depth(code)
        except:
            depth=6*[(0,0)]

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

            if np.mean([i[1] for i in depth[-2:]]) >= np.mean([i[1] for i in depth[:4]]):
                liq +=1
            else:
                liq += 0

        if liq>=1:
            liq='买方力量较大'
        else:
            liq='卖方力量较大'



        # if np.mean([i[1] for i in depth[-2:]]) >= np.mean([i[1] for i in depth[:4]]):
        #     liq='买方力量较大'
        # else:
        #     liq='卖方力量较大'

        if start == 10:
            break
        if ind >= 1:
            return 1, 'upper(next_tick_would_be_lower) 市场深度统计为:'+str(liq)+' 统计委比(近5步)为:%s%%'%np.round(np.mean([i[1] for i in depth])*100,2), float(ti_ck['close']), ti_ck['current_time'],ti_ck['amount']
        elif ind == 0:
            return 1, 'same 市场深度统计为:'+str(liq)+' 统计委比(近5步)为:%s%%'%np.round(np.mean([i[1] for i in depth])*100,2), float(ti_ck['close']), ti_ck['current_time'],float(ti_ck['amount'])
        else  :
            return -1, 'lower(next_tick_would_be_upper) 市场深度统计为'+str(liq)+' 统计委比(近5步)为:%s%%'%np.round(np.mean([i[1] for i in depth])*100,2), float(ti_ck['close']), ti_ck['current_time'],float(ti_ck['amount'])


# codes = ts.get_stock_basics()
import time
import requests

def stifttime(x):
    Serise=pd.Series(x)
    cur = int(re.findall('\d{10}', str(Serise['current_time']))[0])
    timit = time.localtime(cur)
    tim = time.strftime("%Y-%m-%d %H:%M:%S", timit)
    Serise[Serise.index == 'current_time'] =tim
    return  Serise


def get_all_ticker():
    pol = multiprocessing.Pool(processes=100)
    all_close = pol.map(get_current_close, names)
    pol.close()
    pol.join()
    return all_close


def cur_cos_dis(all_ticks):
    alll={}
    for i in range(len(all_ticks.keys())):
        name1=list(all_ticks.keys())[i]
        price1 = all_ticks[name1]
        if len(price1)<=6:
            continue

        for j in range(i,len(all_ticks.keys())):
            name2=list(all_ticks.keys())[j]
            price2=all_ticks[name2]
            if len(price2)<=6:
                continue
            alll['%s_to_%s'%(name1,name2)]=np.arccos(np.dot(price2[-10:],price1[-10:])/(np.linalg.norm(price1[-10:])*np.linalg.norm(price2[-10:])))*(360/3.141592653)
    # alll2={}
    # while 1:
    #     try:
    #         cur=alll.popitem()
    #         if np.nan(cur[1]:
    #             alll2[cur[0]]=cur[1]
    #     except:
    #         break
    return alll



def Main(start, codes,daynight):
    all_ticks = {}
    for i in names:
        all_ticks[i] = []

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
                all_ticker=get_all_ticker()
                #
                try:
                    for i in all_ticker:
                        all_ticks[i[1]].append(i[0])

                    #
                    # pol.join()
                    qqqqq=cur_cos_dis(all_ticks)
                    if len(qqqqq)>1:
                        print('当前所有两两配对距离度量为:',qqqqq)
                    else:
                        print('对比长度还没到',qqqqq)



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
                        hist = huobi_py.get_kline(code, '1day')

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
                            if vol.values[-1] >= vol[:-1].describe()['50%']:
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
                except:
                    continue
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
            time.sleep(30)
            Main(start, codes, daynight)
        except requests.exceptions.ReadTimeout as e:
            print('error api needs rest')
            time.sleep(30)
            Main(start, codes, daynight)
    # writer.save()


#
names=huobi_py.get_symbols()
names=[i['symbol'] for i in names['data']][:12]
Main(5, names,daynight='pm')

# import multiprocessing
# pools=multiprocessing.Pool(processes=150)
# res=[]
# for i in range(len(codes)):
#    res.append(pools.apply_async(Main,(i,codes,'pm')))
# pools.close()
# pools.join()
#

