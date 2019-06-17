# encoding: UTF-8

from logging import INFO

import time
from datetime import datetime



########################################################################
class BaseData(object):
    """回调函数推送数据的基础类，其他数据类继承于此"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor""" 
        self.rawData = None                     # 原始数据

########################################################################
class TsStockData(BaseData):
    """股票数据"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(TsStockData, self).__init__()

        self.code        = ''         # 代码
        self.name        = ''         # 股票名称
        self.area        = ''         # 所在区域
        self.industry    = ''         # 所属行业
        self.exchange    = ''         # 交易所
        self.pe          = ''         # 市盈率
        self.outstanding = ''         # 流通股本(亿)
        self.totals      = ''         # 总股本(亿)
        self.totalAssets = ''         # 总资产(万)
        self.liquidAssets= ''         # 流动资产
        self.fixedAssets = ''         # 固定资产
        self.reserved    = ''         # 公积金
        self.reservedPerShare = ''         # 每股公积金
        self.esp              = ''         # 每股收益 
        self.bvps             = ''         # 每股净资
        self.pb               = ''         # 市净率
        self.timeToMarket     = ''         # 上市日期
        self.undp             = ''         # 未分利润
        self.perundp          = ''         # 每股未分配
        self.rev              = ''         # 收入同比(%)
        self.profit           = ''         # 利润同比(%)
        self.gpr              = ''         # 毛利率(%)
        self.npr              = ''         # 净利润率(%)
        self.holders          = ''         # 股东人数

class tsExchangeCalendar(BaseData):
    """交易日历"""

    #----------------------------------------------------------------------
    def __init__(self):
        super(tsExchangeCalendar, self).__init__()

        self.calendarDate      = ''         # 日历日期
        self.isOpen       = ''         # 是否交易 0休市 1交易










class tsTradeDataDaily(BaseData):
    """日线交易数据"""

    def __init__(self):
        super(tsTradeDataDaily, self).__init__()

        self.code         = ''         # 代码
        self.date         = ''         # 日期
        self.open         = ''         # 开盘价
        self.high         = ''         # 最高价
        self.close        = ''         # 收盘价
        self.low          = ''         # 最低价
        self.volume       = ''         # 成交量
        self.price_change = ''         # 价格变动
        self.p_change     = ''         # 涨跌幅
        self.ma5          = ''         # 5日均价
        self.ma10         = ''         # 10日均价
        self.ma20         = ''         # 20日均价
        self.v_ma5        = ''         # 5日均量
        self.v_ma10       = ''         # 10日均量
        self.v_ma20       = ''         # 20日均量
        self.turnover     = ''         # 换手率
