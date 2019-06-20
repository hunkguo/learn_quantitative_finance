# encoding: UTF-8

from __future__ import print_function
import sys
import json
from datetime import datetime
from time import time, sleep
import tushare as ts

from pymongo import MongoClient, ASCENDING
import pandas as pd
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
    
    cl = db["trade_calendar"]
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



#----------------------------------------------------------------------
def generateTradeCalendar(row):
    """生成交易日历"""
    tc = TsTradeCalendar()
    tc.exchange   = row['exchange']
    tc.cal_date   = row['cal_date']
    tc.is_open    = row['is_open']
    
    return tc


def downloadTradeCalendar():
    """下载交易日历"""

    end_date = (datetime.now()).strftime( "%Y%m%d" ) 
    """下载所有交易日历"""
    tadeCalendar = pro.trade_cal(is_open='1', end_date=end_date)
    cl = db["trade_calendar"]
    cl.create_index([('cal_date', ASCENDING)], unique=True)         # 添加索引
    
    for row in tadeCalendar.iterrows():
        tc = generateTradeCalendar(row[1])
        d = tc.__dict__
        flt = {'cal_date': tc.cal_date}
        cl.replace_one(flt, d, True) 



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
    
    cl = db["stocks"]
    for row in stocks.iterrows():
        stock = generateStock(row[1])
        d = stock.__dict__
        flt = {'ts_code': stock.ts_code}
        cl.replace_one(flt, d, True) 
    cl.create_index([('ts_code', ASCENDING)], unique=True)         # 添加索引





#----------------------------------------------------------------------
def generateTradeDataTick(row):
    """生成历史分笔数据"""
    d = tsTradeDataTick()
    d.ts_code       = row['ts_code']         # TS代码
    d.symbol        = row['symbol']          # 代码
    d.time          = row['time']            # 时间
    d.price         = row['price']           # 成交价格
    d.change        = row['change']          # 价格变动
    d.volume        = row['volume']          # 成交手
    d.amount        = row['amount']          # 成交金额(元)
    d.type          = row['type']            # 买卖类型【买盘、卖盘、中性盘】
    d.trade_date    = row['trade_date']      # 交易日期
    
    return d


#----------------------------------------------------------------------
def downloadTradeDataTick(days):
    """下载历史分笔交易数据"""
    
    cl = db["trade_calendar"]
    # 最近200天交易日
    cals = pd.DataFrame(list(cl.find().sort([('_id', -1)]).limit(days)))
    cals = cals.sort_values(by='cal_date', ascending=True)
    
    cl_stock = db["stocks"]
    stocks = pd.DataFrame(list(cl_stock.find()))

    cl_trade_data_tick = db['trade_data_tick']
    #print(stocks)
    for cal in cals.iterrows():
        for stock in stocks.iterrows():
            date = datetime.strptime(cal[1]['cal_date'], "%Y%m%d").strftime("%Y-%m-%d")
            symbol = stock[1]['symbol']
            tick_data = ts.get_tick_data(symbol,date=date,src='tt')
            tick_data['symbol'] = symbol
            tick_data['ts_code'] = stock[1]['ts_code']
            tick_data['trade_date'] = date

            for row in tick_data.iterrows():
                d = generateTradeDataTick(row[1])
                dd = d.__dict__
                flt = {'time': d.time, 'ts_code': d.ts_code, 'trade_date': d.trade_date}
                cl_trade_data_tick.replace_one(flt, dd, True) 

    cl_trade_data_tick.create_index([('trade_date', ASCENDING), ("ts_code",  ASCENDING), ('time', ASCENDING)], unique=True)         # 添加索引


#----------------------------------------------------------------------
def generateTradeDataRealtimeQuotes(row):
    """生成实时分笔数据"""
    d = tsTradeDataRealtimeQuotes()

    d.ts_code       = row['ts_code']      # TS代码
    d.symbol        = row['code']       # 代码
    d.name          = row['name']         # 股票名字
    d.open          = row['open']         # 今日开盘价
    d.pre_close     = row['pre_close']    # 昨日收盘价
    d.price         = row['price']        # 当前价格
    d.high          = row['high']         # 今日最高价
    d.low           = row['low']          # 今日最低价
    d.bid           = row['bid']          # 竞买价，即“买一”报价
    d.ask           = row['ask']          # 竞卖价，即“卖一”报价
    d.volume        = row['volume']       # 成交量 maybe you need do volume/100
    d.amount        = row['amount']       # 成交金额（元 CNY）
    d.b1_v          = row['b1_v']         # 委买一（笔数 bid volume）
    d.b1_p          = row['b1_p']         # 委买一（价格 bid price）
    d.b2_v          = row['b2_v']         # “买二”
    d.b2_p          = row['b2_p']         # “买二”
    d.b3_v          = row['b3_v']         # “买三”
    d.b3_p          = row['b3_p']         # “买三”
    d.b4_v          = row['b4_v']         # “买四”
    d.b4_p          = row['b4_p']         # “买四”
    d.b5_v          = row['b5_v']         # “买五”
    d.b5_p          = row['b5_p']         # “买五”
    d.a1_v          = row['a1_v']         # 委卖一（笔数 ask volume）
    d.a1_p          = row['a1_p']         # 委卖一（价格 ask price）
    d.a2_v          = row['a2_v']         # 委卖二（笔数 ask volume）
    d.a2_p          = row['a2_p']         # 委卖二（价格 ask price）
    d.a3_v          = row['a3_v']         # 委卖三（笔数 ask volume）
    d.a3_p          = row['a3_p']         # 委卖三（价格 ask price）
    d.a4_v          = row['a4_v']         # 委卖四（笔数 ask volume）
    d.a4_p          = row['a4_p']         # 委卖四（价格 ask price）
    d.a5_v          = row['a5_v']         # 委卖五（笔数 ask volume）
    d.a5_p          = row['a5_p']         # 委卖五（价格 ask price）
    d.date          = row['date']         # 日期；
    d.time          = row['time']         # 时间；
    d.trade_date    = row['trade_date']   # 交易日期
    
    return d



#----------------------------------------------------------------------
def downloadTradeDataRealtimeQuotes():
    """下载历史分笔交易数据"""

    cl_stock = db["stocks"]
    stocks = pd.DataFrame(list(cl_stock.find()))

    today = (datetime.now()).strftime('%Y%m%d')

    cl_trade_data_realtime_quotes = db['trade_data_realtime_quotes']

    for stock in stocks.iterrows():
        symbol = stock[1]['symbol']
        realtime_quotes_data = ts.get_realtime_quotes(symbol)
        realtime_quotes_data['ts_code'] = stock[1]['ts_code']
        realtime_quotes_data['trade_date'] = today
        #print(realtime_quotes_data)

        for row in realtime_quotes_data.iterrows():
            d = generateTradeDataRealtimeQuotes(row[1])
            dd = d.__dict__
            flt = {'time': d.time, 'ts_code': d.ts_code, 'trade_date': d.trade_date}
            cl_trade_data_realtime_quotes.replace_one(flt, dd, True) 
    
    cl_trade_data_realtime_quotes.create_index([('trade_date', ASCENDING), ("ts_code",  ASCENDING), ('time', ASCENDING)], unique=True)         # 添加索引
