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
#from sshtunnel import SSHTunnelForwarder
from model.tsObject import tsTradeDataDaily,TsStockData,TsTradeCalendar,tsTradeDataTick,tsTradeDataRealtimeQuotes
from tsCommon import *
from operator import itemgetter

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

        
def test2():
    trade_date = getTradeDate(1)
    trade_date_ts = getTradeDate(1, type='ts')


    # 取涨停股票
    daily_data = pro.daily(trade_date=trade_date, fields='ts_code, pct_chg, pre_close')
    stocks_limit_up = daily_data[(daily_data['pct_chg'] > 9.0)]

    for stock in stocks_limit_up.iterrows():
        sleep(0.5)
        ts_code = stock[1]['ts_code']
        #print(stock[1]['ts_code'].split(".", 1)[0])
        symbol = ts_code.split(".", 1)[0]
        tick_data = ts.get_tick_data(symbol,date=trade_date_ts,src='tt')
        tick_data_group = tick_data.groupby(by=['price', 'type'])
        tick_data_group_sum_volume = tick_data_group['volume'].sum().to_frame() 
        tick_data_group_sum_amount = tick_data_group['amount'].sum().to_frame() 

        tick_data_calculation = pd.merge(tick_data_group_sum_volume,tick_data_group_sum_amount,left_index=True,right_index=True,how='outer')

        
        tick_data_calculation['占比'] = ((tick_data_calculation['volume']/tick_data_calculation['volume'].sum()).round(decimals=2)).map(lambda x: format(x, '.0%'))

        # 计算涨停价
        limit_up_price = round(stock[1]['pre_close'] * 1.1, 2)
        # 涨停价成交量
        limit_up_volume = tick_data_calculation.loc[limit_up_price, ['volume']]
        if(len(limit_up_volume.loc['买盘'])>0):
            limit_up_volume_buy = (limit_up_volume.loc['买盘'])['volume']
        if(len(limit_up_volume.loc['卖盘'])>0):
            limit_up_volume_sell = (limit_up_volume.loc['卖盘'])['volume']

        #print(type(stock['limit_up_price']))
        # 板上成交额
        stocks_limit_up.loc[stocks_limit_up.ts_code == ts_code,"limit_up_amount"] = (limit_up_price * (limit_up_volume_buy + limit_up_volume_buy))
        # 板上内外比  买盘/卖盘
        stocks_limit_up.loc[stocks_limit_up.ts_code == ts_code,"limit_up_volume_per"] = round(limit_up_volume_buy/limit_up_volume_sell, 2)
        # 达到涨停价时间
        stocks_limit_up.loc[stocks_limit_up.ts_code == ts_code,"limit_up_time"] = list((tick_data[(tick_data['price']==limit_up_price)]).head(1).loc[:, 'time'])[0]
        #print(stocks_limit_up.loc[stocks_limit_up.ts_code == ts_code])

    print(stocks_limit_up)
    stocks_limit_up.to_csv('Result.csv')
        


if __name__ == '__main__':
    test2()
# 判断交易时间，是否使用当天数据



'''取涨停股票的概念分类和行业，完成

    # 股票基础数据 取行业
    stocks_basic_data = pro.stock_basic(exchange='', list_status='L', fields='ts_code, industry')
    # print(stocks[(stocks['ts_code'] == '603997.SH')])
    # 概念股分类 
    concept_data = pro.concept(src='ts', fields='name')
    # 初始化 概念分类 字典
    concept_data_dict = dict()
    stock_basic_data_1 = pd.DataFrame(columns = ["ts_code", "industry"])
    for concept in concept_data.iterrows():
        concept_name = concept[1]['name']
        concept_data_dict[concept_name] = 0

    trade_date = getTradeDate(1)

    daily_data = pro.daily(trade_date=trade_date, fields='ts_code, pct_chg')
    stocks_limit_up = daily_data[(daily_data['pct_chg'] > 9.0)]

    for index,stock in stocks_limit_up.iterrows():
        sleep(0.5)
        ts_code = stock['ts_code']
        stock_concept = pro.concept_detail(ts_code = ts_code, fields='concept_name')
        for sc in stock_concept.iterrows():
            sc_name = sc[1]['concept_name']
            concept_data_dict[sc_name] += 1
        
        stock_basic_code = stocks_basic_data[(stocks_basic_data['ts_code']==ts_code)]
        stock_basic_data_1 = stock_basic_data_1.append(stock_basic_code)
        if(index > 100):
            break

    #sorted_dict = sorted(concept_data_dict.items(), key=lambda item: item[1], reverse=True)
    concept_df = pd.DataFrame(list(concept_data_dict.items()), columns=['concept_name', 'count'])

    print(concept_df[(concept_df['count']>0)])
    print(stock_basic_data_1)
'''