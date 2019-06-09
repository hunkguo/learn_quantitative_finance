# encoding: UTF-8

from __future__ import print_function
import sys
import json
from datetime import datetime
from time import time, sleep
import tushare as ts

from pymongo import MongoClient, ASCENDING

import tushare as ts


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

def downloadAllStock():
    """下载所有股票信息"""
    print('-' * 50)
    print(u'开始下载股票数据')
    print('-' * 50)
    stocks = pro.stock_basic(exchange='', list_status='L')
    #选股 条件3 非ST股票
    stocks = stocks[~stocks.name.str.contains('ST')]
    
    cl = db["symbols"]
    stocks_bson = json.loads(stocks.T.to_json()).values()
    
    try:
        cl.insert_many(stocks_bson, True) 
    except:
        cl.update_many(stocks_bson, True) 
    
    print('-' * 50)
    print(u'股票数据下载完成')
    print('-' * 50)

'''
                                    cl = db[symbol]
                                    cl.ensure_index([('datetime', ASCENDING)], unique=True)         # 添加索引
                                    
                                    df = ts.bar(symbol, freq='1min')
                                    df = df.sort_index()
                                    
                                    for ix, row in df.iterrows():
                                        bar = generateVtBar(row)
                                        d = bar.__dict__
                                        flt = {'datetime': bar.datetime}
                                        cl.replace_one(flt, d, True)  
'''

if __name__ == '__main__':
    downloadAllStock()