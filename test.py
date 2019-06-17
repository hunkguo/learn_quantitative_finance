# encoding: UTF-8

from __future__ import print_function
import sys
import json
from datetime import datetime
from time import time, sleep
import tushare as ts

from pymongo import MongoClient, ASCENDING
import pandas as pd
from model.tsObject import tsTradeDataDaily,TsStockData,TsTradeCalenday

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

    df = ts.get_tick_data('600848',date='2018-12-12',src='tt')
    df.head(10)
    print(df)


if __name__ == '__main__':
    #downloadAllStock()
    test()