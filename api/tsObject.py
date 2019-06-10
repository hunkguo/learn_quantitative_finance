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

        self.ts_code   = ''         # TS代码
        self.symbol    = ''         # 代码
        self.exchange  = ''         # 交易所
        self.name      = ''         # 股票名称
        self.area      = ''         # 所在区域
        self.industry  = ''         # 所属行业
        self.market    = ''         # 市场类型 （主板/中小板/创业板）
        self.list_date = ''         # 上市日期

class TsTradeCalenday(BaseData):
    """交易日历"""

    #----------------------------------------------------------------------
    def __init__(self):
        super(TsTradeCalenday, self).__init__()

        self.exchange      = ''         # 交易所
        self.cal_date      = ''         # 日历日期
        self.is_open       = ''         # 是否交易 0休市 1交易


class tsTradeDataDaily(BaseData):
    """日线交易数据"""

    def __init__(self):
        super(tsTradeDataDaily, self).__init__()

        self.ts_code       = ''         # TS代码
        self.trade_date    = ''         # 交易日期
        self.open          = ''         # 开盘价
        self.high          = ''         # 最高价
        self.low           = ''         # 最低价
        self.close         = ''         # 收盘价
        self.pre_close     = ''         # 昨收价
        self.change        = ''         # 涨跌额
        self.pct_chg       = ''         # 涨跌幅 （未复权，如果是复权请用 通用行情接口 ）
        self.vol           = ''         # 成交量 （手）
        self.amount        = ''         # 成交额 （千元）