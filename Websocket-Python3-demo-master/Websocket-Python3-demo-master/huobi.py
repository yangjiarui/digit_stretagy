# -*- coding: utf-8 -*-
#author: jerry

from websocket import create_connection
import gzip
import time
import json,time,re
import pandas as pd
import matplotlib.pyplot as plt
#if __name__ == '__main__':
while(1):
    try:
        ws = create_connection("wss://api.huobipro.com/ws")
        break
    except:
        print('connect ws error,retry...')
        time.sleep(5)

# 订阅 KLine 数据
#tradeStr="""{"sub": "market.btcusdt.kline.1min","id": "id10"}"""

# 请求 KLine 数据
#tradeStr="""{"req": "market.ethusdt.kline.1week","id": "id10", "from": 1513391453, "to": 1513392453}"""

#订阅 Market Depth 数据
# tradeStr="""{"sub": "market.ethusdt.depth.step5", "id": "id10"}"""

#请求 Market Depth 数据
# tradeStr="""{"req": "market.ethusdt.depth.step5", "id": "id10"}"""

#订阅 Trade Detail 数据
#x1=input('请输入您想查看的币种')
#x2=input('请输入您想从中查找的平台')
# tradeStr="""{"sub": "market.btcusdt.trade.detail", "id": "id10"}"""

#请求 Trade Detail 数据
#tradeStr="""{"req": "market.htusdt.trade.detail", "id": "id10"}"""

#请求 Market Detail 数据
#tradeStr="""{"req": "market.ethusdt.detail", "id": "id12"}"""
# for i in range(6):
#     ws.send(tradeStr)
#     compressData = ws.recv()
#     result = gzip.decompress(compressData).decode('utf-8')
#     hh = result
#     # print(result)
#     if result[:7] == '{"ping"':
#         ts = result[8:21]
#         pong = '{"pong":' + ts + '}'
#         ws.send(pong)
#         ws.send(tradeStr)
#     else:
#         # print('reg',result)
#         q = json.loads(result)
#         #print(q)

#tradeStr = """{"sub": "market.btcusdt.trade.detail", "id": "id10"}"""
lis=pd.read_csv('/home/jerry/PycharmProjects/blochain/huobi_symbols_range.csv')
lis=lis.iloc[:,1].values
def sub_trade_detail(Num):
    global lis
    strings=lis[Num].lower()
    c=strings.split('/')
    strings=c[0]+c[1]
    tradeStr = """{"sub": "market.%s.trade.detail", "id": "id10"}"""%strings

    full=pd.DataFrame(columns=['分子与分母币种','价格','当前时间','交易方向','数量'])
    ws.send(tradeStr)
    #k=0
    #plt.ion()
    #plt.figure(2)
    draw_price,draw_amonut=[],[]
    while 1:
        #time.sleep(0.002)
        #k += 1
        compressData=ws.recv()
        result=gzip.decompress(compressData).decode('utf-8')
        hh=result
        #print(result)
        if result[:7] == '{"ping"':
            ts=result[8:21]
            pong='{"pong":'+ts+'}'
            ws.send(pong)
            ws.send(tradeStr)
        else:
            #print('reg',result)
            q=json.loads(result)

            if 'ch' in list(q.keys()):
                cur=q['tick']['data'][0]['ts']
                cur=int(re.findall('\d{10}',str(cur))[0])
                timit=time.localtime(cur)
                tim=time.strftime("%Y-%m-%d %H:%M:%S", timit)
                name=q[list(q.keys())[0]].split('.')[1]
                price=q['tick']['data'][0]['price']
                direction=q['tick']['data'][0]['direction']
                amonut=q['tick']['data'][0]['amount']
                hh=pd.Series([name,price,tim,direction,amonut],index=['分子与分母币种','价格','当前时间','交易方向','数量'])
                full=full.append(hh,ignore_index=True)
                print('Done %s %s %s'%(tim,price,name))
                #draw_amonut.append(amonut)
                #draw_price.append(price)
#                plt.subplot(211)
#                plt.title('price')
#                plt.plot(draw_price,label='price')
#                plt.grid(True)
#                plt.subplot(212)
#                plt.title('amount')
#                plt.plot(draw_amonut,label='amount')
#                plt.grid(True)
#
#                plt.draw()
#                time.sleep(1)
        if  time.strftime("%X",time.localtime())>='13:41:00':
           break
    full.index = pd.DatetimeIndex(full.iloc[:, 2])
    full = full.iloc[:, [0, 1, 3, 4]]
    full = full.resample('3s', 'mean')
    print('nkdhsfukhukvnkefnve')
    return full


import multiprocessing
# # #
# pools=multiprocessing.Pool(processes=10)
# res=[]
# for z in range(len(lis)):
#     res.append(pools.apply_async(sub_trade_detail,args=(z,)))
#
# pools.close()
# pools.join()
qq=sub_trade_detail(Num=3)













         #if result[:7] == '{"ping"':
#            ts=result[8:21]
#            pong='{"pong":'+ts+'}'
#            ws.send(pong)
#            ws.send(tradeStr)
#        else:
#            print('reg',result)
#            q=json.loads(result)
#            print(q)
           
