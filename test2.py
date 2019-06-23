# encoding: UTF-8

from __future__ import print_function
import sys
import json
from datetime import datetime
from time import time, sleep
import tushare as ts

from pymongo import MongoClient, ASCENDING
import pandas as pd

# 加载配置
config = open("config.json")
setting = json.load(config)

MONGO_HOST = setting['MONGO_HOST']
MONGO_PORT = setting['MONGO_PORT']
Tushare_TOKEN = setting['Tushare_TOKEN']
MONGO_DB = setting['MONGO_DB']

mc = MongoClient(MONGO_HOST, MONGO_PORT)        # Mongo连接
db = mc[MONGO_DB]        

pro = ts.pro_api(Tushare_TOKEN)



def test():
    """仅用于测试"""

#    stocks_data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name')
#    for row in stocks_data.iterrows():
#        ts_code = row[1]['ts_code']
#        stock_daily_data = pro.daily(ts_code=ts_code, start_date='20190619', end_date='20190619')
#        pct_chg = stcok_daily_data
#        print(df)
#        break

    daily_data = pro.daily(trade_date='20190619')
    stocks_limit_up = daily_data[(daily_data['pct_chg'] > 9.0)]
    #print(stocks_limit_up)
    for stock in stocks_limit_up.iterrows():
        print(stock[1]['ts_code'])

if __name__ == '__main__':
    #downloadAllStock()
    test()
