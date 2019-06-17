# encoding: UTF-8

from __future__ import print_function
import sys
import json
from datetime import datetime
from time import time, sleep
import tushare as ts

from pymongo import MongoClient, ASCENDING
import pandas as pd
from model.tsObject import tsTradeDataDaily,TsStockData,tsExchangeCalendar

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
def generateExchangeCalendar(row):
    """生成交易日历"""
    tec = tsExchangeCalendar()
    tec.calendarDate   = row['calendarDate']
    tec.isOpen    = row['isOpen']
    
    return tec


#----------------------------------------------------------------------
def downloadExchangeCalendar():
    """下载所有交易日历"""
    cal_dates = ts.trade_cal()
    ec = db["exchange_calendar"]
    today = (datetime.now()).strftime('%Y-%m-%d')
    for row in cal_dates.iterrows():
        tec = generateExchangeCalendar(row[1])
        d = tec.__dict__
        flt = {'calendarDate': tec.calendarDate}
        ec.replace_one(flt, d, True) 
        if(tec.calendarDate ==today):
            break

    ec.create_index([('calendarDate', ASCENDING)], unique=True)         # 添加索引
    


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
    stock.code      = row[0]
    stock.name      = row[1]['name']
    stock.area      = row[1]['area']
    stock.industry  = row[1]['industry']
    stock.exchange  = generateExchange(stock.code)
    stock.pe          = row[1]['pe']
    stock.outstanding = row[1]['outstanding']         # 流通股本(亿)
    stock.totals      = row[1]['totals']         # 总股本(亿)
    stock.totalAssets = row[1]['totalAssets']         # 总资产(万)
    stock.liquidAssets= row[1]['liquidAssets']         # 流动资产
    stock.fixedAssets = row[1]['fixedAssets']         # 固定资产
    stock.reserved    = row[1]['reserved']         # 公积金
    stock.reservedPerShare = row[1]['reservedPerShare']         # 每股公积金
    stock.esp              = row[1]['esp']         # 每股收益 
    stock.bvps             = row[1]['bvps']         # 每股净资
    stock.pb               = row[1]['pb']         # 市净率
    stock.timeToMarket     = row[1]['timeToMarket']         # 上市日期
    stock.undp             = row[1]['undp']         # 未分利润
    stock.perundp          = row[1]['perundp']         # 每股未分配
    stock.rev              = row[1]['rev']         # 收入同比(%)
    stock.profit           = row[1]['profit']         # 利润同比(%)
    stock.gpr              = row[1]['gpr']         # 毛利率(%)
    stock.npr              = row[1]['npr']         # 净利润率(%)
    stock.holders          = row[1]['holders']         # 股东人数
    
    return stock


def downloadAllStock():
    """下载所有股票信息"""

    stocks = ts.get_stock_basics()
    cl = db["stocks"]
    for row in stocks.iterrows():
        stock = generateStock(row)
        d = stock.__dict__
        flt = {'code': stock.code}
        cl.replace_one(flt, d, True) 
    
    cl.create_index([('code', ASCENDING)], unique=True)         # 添加索引

























#----------------------------------------------------------------------
def generateTradeDataDaily(row):
    """生成交易数据"""
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


    tc.code         = ''         # 代码
    tc.date         = ''         # 日期
    tc.open         = ''         # 开盘价
    tc.high         = ''         # 最高价
    tc.close        = ''         # 收盘价
    tc.low          = ''         # 最低价
    tc.volume       = ''         # 成交量
    tc.price_change = ''         # 价格变动
    tc.p_change     = ''         # 涨跌幅
    tc.ma5          = ''         # 5日均价
    tc.ma10         = ''         # 10日均价
    tc.ma20         = ''         # 20日均价
    tc.v_ma5        = ''         # 5日均量
    tc.v_ma10       = ''         # 10日均量
    tc.v_ma20       = ''         # 20日均量
    tc.turnover     = ''         # 换手率
    
    return tc


def downloadTradeDataDaily(days):
    """下载所有日线交易数据"""
    
    cl = db["exchange_calendar"]
    cals = pd.DataFrame(list(cl.find({'isOpen': 1}).sort([('_id', -1)]).limit(10)))
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
        tradeDataDaily['code'] = stock[1]['code']
        print(tradeDataDaily)
        break

'''
    cl_tradedata = db["trade_data_daily"]
    cl_tradedata.create_index([('trade_date', ASCENDING), ("ts_code",  ASCENDING)], unique=True)         # 添加索引
    #print(cals.tail(200))
    
    for cal in cals.iterrows():
        #print(cal[1])
        
        trade_date = cal[1]['cal_date']
        #print(trade_date)
        tradeData = ts.get_hist_data
        for row in tradeData.iterrows():
            td = generateTradeDataDaily(row[1])
            #print(row[1])
            d = td.__dict__
            #print(td.trade_date)
            flt = {'trade_date': td.trade_date, 'ts_code': td.ts_code}
            cl_tradedata.replace_one(flt, d, True) 

'''





