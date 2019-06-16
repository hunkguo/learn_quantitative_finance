# encoding: UTF-8

from __future__ import print_function
import sys
import json
from datetime import datetime
from time import time, sleep
import tushare as ts

from pymongo import MongoClient, ASCENDING
import pandas as pd
import easyquotation

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



#----------------------------------------------------------------------
def tickData(d):
    """下载历史分笔数据"""
    
    # df = pro.get_tick_data('600848',date=d)
    # df = pro.get_realtime_quotes('000581')
    quotation = easyquotation.use('sina') # 新浪 ['sina'] 腾讯 ['tencent', 'qq'] 
    
    stocks = pd.DataFrame(list(db["stocks"].find()))

    for stock in stocks.iterrows():
        symbol = stock[1]['symbol']

        stock_data_sina = quotation.real(symbol, prefix=True)
        print(type(stock_data_sina))
        break

if __name__ == '__main__':
    tickData('2019-6-14')
