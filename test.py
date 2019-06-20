# encoding: UTF-8

from __future__ import print_function
import sys
import json
from datetime import datetime
from time import time, sleep
import tushare as ts

from pymongo import MongoClient, ASCENDING
import pandas as pd
from sshtunnel import SSHTunnelForwarder
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
    

pro = ts.pro_api(Tushare_TOKEN)


def test():
    """仅用于测试"""     


    # define ssh tunnel
    server = SSHTunnelForwarder(
        (SERVER_HOST, SERVER_PORT),
        ssh_username=SERVER_USER,
        # ssh_password=MONGO_PASS,
        ssh_pkey="/Users/hunk/zbq.pem",
        remote_bind_address=(MONGO_HOST, MONGO_PORT)
    )



    # start ssh tunnel
    server.start()

    mc = MongoClient(MONGO_HOST, server.local_bind_port)        # Mongo连接
    db = mc[MONGO_DB]  


    cl_stock = db["stocks"]
    stocks = pd.DataFrame(list(cl_stock.find()))
    print(stocks)

    print('_'*50)
    # close ssh tunnel
    server.close()
    

    print('+'*50)


'''
    for stock in stocks.iterrows():
        symbol = stock[1]['symbol']
        print(symbol)
'''    
        
def test2():

    today = datetime.now().strftime('%Y%m%d')
    print(today)

    daily_data = pro.daily(trade_date='20190619')
    stocks_limit_up = daily_data[(daily_data['pct_chg'] > 9.0)]
    #print(stocks_limit_up)
    for stock in stocks_limit_up.iterrows():
        print(stock[1]['ts_code'])


if __name__ == '__main__':
    test2()


 


    
    
    