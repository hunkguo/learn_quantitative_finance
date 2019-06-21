# encoding: UTF-8

from __future__ import print_function
import sys
import json
from datetime import datetime
from time import time, sleep
import tushare as ts
from collections import Counter
from pymongo import MongoClient, ASCENDING
import pandas as pd
from sshtunnel import SSHTunnelForwarder
from model.tsObject import tsTradeDataDaily,TsStockData,TsTradeCalendar,tsTradeDataTick,tsTradeDataRealtimeQuotes

# 加载配置
config = open("config.json")
setting = json.load(config)

MONGO_HOST = setting['MONGO_HOST']
MONGO_PORT = setting['MONGO_PORT']
Tushare_TOKEN = setting['Tushare_TOKEN']
MONGO_DB = setting['MONGO_DB']

SERVER_HOST = setting['SERVER_HOST']
SERVER_PORT = setting['SERVER_PORT']
SERVER_USER = setting['SERVER_USER']
    

pro = ts.pro_api(Tushare_TOKEN)


def test():
    """仅用于测试"""     


    # define ssh tunnel
    server = SSHTunnelForwarder(
        (SERVER_HOST, SERVER_PORT),
        ssh_username=SERVER_USER,
        # ssh_password=MONGO_PASS,
        ssh_pkey="/Users/hunk/zbq.pem",
        remote_bind_address=(MONGO_HOST, MONGO_PORT)
    )



    # start ssh tunnel
    server.start()

    mc = MongoClient(MONGO_HOST, server.local_bind_port)        # Mongo连接
    db = mc[MONGO_DB]  


    cl_stock = db["stocks"]
    stocks = pd.DataFrame(list(cl_stock.find()))
    print(stocks)

    print('_'*50)
    # close ssh tunnel
    server.close()
    

    print('+'*50)


'''
    for stock in stocks.iterrows():
        symbol = stock[1]['symbol']
        print(symbol)
'''    
        
def test2():

    # 当前日期 待修改，根据时间判断交易日
    today = datetime.now().strftime('%Y%m%d')
    # print(today)
    tradeCalendar = pro.trade_cal(is_open='1', end_date=today)
    tradeCalendar = tradeCalendar.tail(4)
    tradeCalendar = tradeCalendar.sort_values(by='cal_date', ascending=True)
    print(tradeCalendar)





    # 概念分类
    concept_classified_data = ts.get_concept_classified()
    concept_classified_data = concept_classified_data.set_index('code')['c_name'].to_dict()

    # concept_classified_count = Counter()
    concept_classified_count = {}

    daily_data = pro.daily(trade_date=today)
    stocks_limit_up = daily_data[(daily_data['pct_chg'] > 9.0)]
    #print(stocks_limit_up)
    for stock in stocks_limit_up.iterrows():
        #print(stock[1]['ts_code'].split(".", 1)[0])
        symbol = stock[1]['ts_code'].split(".", 1)[0]
        # concept_classified_count.update(str(concept_classified_data[symbol])

#        if (concept_classified_count(concept_classified_data[symbol]) == 0):
#           concept_classified_count.update(concept_classified_data[symbol])
        if (symbol in concept_classified_data and concept_classified_data[symbol] in concept_classified_count):
            concept_classified_count[concept_classified_data[symbol]] += 1
        elif(symbol in concept_classified_data):
            concept_classified_count[concept_classified_data[symbol]] = 1
        
    # print(concept_classified_count)

    # df = pd.DataFrame.from_dict(concept_classified_count, orient='index', columns=['涨停数量'])
    df = pd.DataFrame(list(concept_classified_count.items()), columns=['概念分类', '涨停数量'])
    print(df.sort_values(by='涨停数量', ascending=False))

    

        


if __name__ == '__main__':
    test2()
# 判断交易时间，是否使用当天数据



# 分价表
# -----------------------------------------------------------------------------------------
'''
    tick_data = ts.get_tick_data('300362',date='2019-06-20',src='tt')
    tick_data_group = tick_data.groupby(['price', 'type'])
    tick_data_group_sum_volume = tick_data_group['volume'].sum().to_frame() 
    tick_data_group_sum_amount = tick_data_group['amount'].sum().to_frame() 

    df = pd.merge(tick_data_group_sum_volume,tick_data_group_sum_amount,left_index=True,right_index=True,how='outer')
    df['占比'] = ((df['volume']/df['volume'].sum()).round(decimals=2)).map(lambda x: format(x, '.0%'))
    print(df)






    today = datetime.now().strftime('%Y%m%d')
    #print(today)

    daily_data = pro.daily(trade_date='20190619')
    stocks_limit_up = daily_data[(daily_data['pct_chg'] > 9.0)]
    #print(stocks_limit_up)
    for stock in stocks_limit_up.iterrows():
        #print(stock[1]['ts_code'].split(".", 1)[0])
        symbol = stock[1]['ts_code'].split(".", 1)[0]
        tick_data = ts.get_tick_data(symbol,date='2018-12-12',src='tt')
        tick_data_group = tick_data.groupby(by=['price'])
        tick_data_group_sum_volume = tick_data_group['volume'].sum().to_frame() 
        tick_data_group_sum_amount = tick_data_group['amount'].sum().to_frame() 

        df = pd.merge(tick_data_group_sum_volume,tick_data_group_sum_amount,left_index=True,right_index=True,how='outer')
        print(df)
        break


# 概念分类 字典
# -----------------------------------------------------------------------------------------

    df = ts.get_concept_classified()
    dict_country = df.set_index('code')['c_name'].to_dict()
    print(dict_country['002633'])
'''