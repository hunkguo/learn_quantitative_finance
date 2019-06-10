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
def generateTradeCalenday(row):
    """生成交易日历"""
    tc = TsTradeCalenday()
    tc.exchange   = row['exchange']
    tc.cal_date   = row['cal_date']
    tc.is_open    = row['is_open']
    
    return tc


def downloadTradeCalenday():
    """下载所有交易日历"""
    tadeCalenday = pro.trade_cal(is_open='1'  )
    #选股 条件3 非ST股票
    
    cl = db["trade_calenday"]
    #print(tadeCalenday)
    cl.create_index([('cal_date', ASCENDING)], unique=True)         # 添加索引
    
    for row in tadeCalenday.iterrows():
        tc = generateTradeCalenday(row[1])
        d = tc.__dict__
        flt = {'cal_date': tc.cal_date}
        cl.replace_one(flt, d, True) 
    
