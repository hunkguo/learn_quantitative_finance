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




#----------------------------------------------------------------------
def tickData(d):
    
    cl = db["exchange_calendar"]
    cals = pd.DataFrame(list(cl.find({'isOpen': 1}).sort([('_id', -1)]).limit(100)))
    cals = cals.sort_values(by='calendarDate', ascending=True)
    start_date = cals.loc[len(cals)-1]['calendarDate']
    end_date = cals.loc[0]['calendarDate']
    print(start_date)
    print(end_date)
    cl_stock = db["stocks"]
    stocks = pd.DataFrame(list(cl_stock.find()))
    for stock in stocks.iterrows():
        #print(stock[1]['code'])
        tradeDataDaily = ts.get_hist_data(stock[1]['code'],start=start_date,end=end_date)
        # tradeDataDaily['code'] = stock[1]['code']
        print(len(tradeDataDaily))
        break

if __name__ == '__main__':
    # tickData('2019-6-14')
    df = ts.get_tick_data('600848',date='2019-06-12',src='tt')
    #df = ts.get_hist_data('600848')
    print(df)
