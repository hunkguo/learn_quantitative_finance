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

Tushare_TOKEN = setting['Tushare_TOKEN']
pro = ts.pro_api(Tushare_TOKEN)



def getTradeDate(N, type=''):
    today = datetime.now().strftime('%Y%m%d')
    tradeDate_data = pro.trade_cal(exchange='', end_date=today, is_open='1')
    
    if(type==''):
        return tradeDate_data.loc[len(tradeDate_data)-N, 'cal_date']
    elif(type=='ts'):
        newTradeDate = datetime.strptime(tradeDate_data.loc[len(tradeDate_data)-N, 'cal_date'], '%Y%m%d')
        
        return newTradeDate.strftime('%Y-%m-%d')

if __name__ == '__main__':
    getTradeDate(10)
