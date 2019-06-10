# encoding: UTF-8

from __future__ import print_function
import sys
import json
from datetime import datetime
from time import time, sleep
import tushare as ts

from pymongo import MongoClient, ASCENDING

import tushare as ts

from api.tsObject import *

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
def generateExchange(symbol):
    """生成交易所代码"""
    if symbol[0:2] in ['60', '51']:
        exchange = 'SSE'
    elif symbol[0:2] in ['00', '15', '30']:
        exchange = 'SZSE'
    return exchange

#----------------------------------------------------------------------
def generateStock(row):
    """生成股票数据"""
    stock = TsStockData()
    stock.ts_code   = row['ts_code']
    stock.symbol    = row['symbol']
    stock.exchange  = generateExchange(stock.symbol)
    stock.name      = row['name']
    stock.area      = row['area']
    stock.industry  = row['industry']
    stock.market    = row['market']
    stock.list_date = row['list_date']
    
    return stock


def downloadAllStock():
    """下载所有股票信息"""
    stocks = pro.stock_basic(exchange='', list_status='L')
    #选股 条件3 非ST股票
    stocks = stocks[~stocks.name.str.contains('ST')]
    
    cl = db["symbols"]
    cl.create_index([('ts_code', ASCENDING)], unique=True)         # 添加索引
    for row in stocks.iterrows():
        stock = generateStock(row[1])
        d = stock.__dict__
        flt = {'ts_code': stock.ts_code}
        cl.replace_one(flt, d, True) 

