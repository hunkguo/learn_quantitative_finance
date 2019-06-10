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

#----------------------------------------------------------------------
def generateTradeDataDaily(row):
    """生成交易日历"""
    tc = tsTradeDataDaily()
    tc.ts_code   = row['ts_code']
    tc.trade_date   = row['trade_date']
    tc.open    = row['open']
    tc.high   = row['high']
    tc.low   = row['low']
    tc.close   = row['close']
    tc.pre_close   = row['pre_close']
    tc.change   = row['change']
    tc.pct_chg   = row['pct_chg']
    tc.vol   = row['vol']
    tc.amount   = row['amount']
    
    return tc


def downloadTradeDataDaily(days):
    """下载所有日线交易数据"""
    
    print('-' * 50)
    print('开始下载日线交易数据')
    cl = db["trade_calenday"]
    # 最近200天交易日
    cals = pd.DataFrame(list(cl.find().sort([('_id', -1)]).limit(days)))
    cals = cals.sort_values(by='cal_date', ascending=True)


    cl_tradedata = db["trade_data_daily"]
    cl_tradedata.create_index([('trade_date', ASCENDING), ("ts_code",  ASCENDING)], unique=True)         # 添加索引
    #print(cals.tail(200))
    
    for cal in cals.iterrows():
        #print(cal[1])
        
        trade_date = cal[1]['cal_date']
        #print(trade_date)
        tradeData = pro.daily(trade_date=trade_date)
        for row in tradeData.iterrows():
            td = generateTradeDataDaily(row[1])
            #print(row[1])
            d = td.__dict__
            #print(td.trade_date)
            flt = {'trade_date': td.trade_date, 'ts_code': td.ts_code}
            cl_tradedata.replace_one(flt, d, True) 
    print('-' * 50)



#----------------------------------------------------------------------
def generateTradeCalenday(row):
    """生成交易日历"""
    tc = TsTradeCalenday()
    tc.exchange   = row['exchange']
    tc.cal_date   = row['cal_date']
    tc.is_open    = row['is_open']
    
    return tc


def downloadTradeCalenday():
    """下载交易日历"""

    print('-' * 50)
    print(u'开始下载交易日历数据')
    end_date = (datetime.now()).strftime( "%Y%m%d" ) 
    """下载所有交易日历"""
    tadeCalenday = pro.trade_cal(is_open='1', end_date=end_date)
    cl = db["trade_calenday"]
    #print(tadeCalenday)
    cl.create_index([('cal_date', ASCENDING)], unique=True)         # 添加索引
    
    for row in tadeCalenday.iterrows():
        tc = generateTradeCalenday(row[1])
        d = tc.__dict__
        flt = {'cal_date': tc.cal_date}
        cl.replace_one(flt, d, True) 
    print('-' * 50)



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

    print('-' * 50)
    print('开始下载股票数据')
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
    print('-' * 50)



