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

class TsTradeCalendar(BaseData):
    """交易日历"""

    #----------------------------------------------------------------------
    def __init__(self):
        super(TsTradeCalendar, self).__init__()

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


class tsTradeDataTick(BaseData):
    """历史分笔交易数据"""

    def __init__(self):
        super(tsTradeDataTick, self).__init__()

        self.ts_code       = ''         # TS代码
        self.symbol        = ''         # 代码
        self.time          = ''         # 时间
        self.price         = ''         # 成交价格
        self.change        = ''         # 价格变动
        self.volume        = ''         # 成交手
        self.amount        = ''         # 成交金额(元)
        self.type          = ''         # 买卖类型【买盘、卖盘、中性盘】
        self.trade_date    = ''         # 交易日期

class tsTradeDataRealtimeQuotes(BaseData):
    """实时分笔数据"""

    def __init__(self):
        super(tsTradeDataRealtimeQuotes, self).__init__()

        self.ts_code       = ''         # TS代码
        self.symbol        = ''         # 代码
        self.name          = ''         # 股票名字
        self.open          = ''         # 今日开盘价
        self.pre_close     = ''         # 昨日收盘价
        self.price         = ''         # 当前价格
        self.high          = ''         # 今日最高价
        self.low           = ''         # 今日最低价
        self.bid           = ''         # 竞买价，即“买一”报价
        self.ask           = ''         # 竞卖价，即“卖一”报价
        self.volume        = ''         # 成交量 maybe you need do volume/100
        self.amount        = ''         # 成交金额（元 CNY）
        self.b1_v          = ''         # 委买一（笔数 bid volume）
        self.b1_p          = ''         # 委买一（价格 bid price）
        self.b2_v          = ''         # “买二”
        self.b2_p          = ''         # “买二”
        self.b3_v          = ''         # “买三”
        self.b3_p          = ''         # “买三”
        self.b4_v          = ''         # “买四”
        self.b4_p          = ''         # “买四”
        self.b5_v          = ''         # “买五”
        self.b5_p          = ''         # “买五”
        self.a1_v          = ''         # 委卖一（笔数 ask volume）
        self.a1_p          = ''         # 委卖一（价格 ask price）
        self.a2_v          = ''         # 委卖二（笔数 ask volume）
        self.a2_p          = ''         # 委卖二（价格 ask price）
        self.a3_v          = ''         # 委卖三（笔数 ask volume）
        self.a3_p          = ''         # 委卖三（价格 ask price）
        self.a4_v          = ''         # 委卖四（笔数 ask volume）
        self.a4_p          = ''         # 委卖四（价格 ask price）
        self.a5_v          = ''         # 委卖五（笔数 ask volume）
        self.a5_p          = ''         # 委卖五（价格 ask price）
        self.date          = ''         # 日期；
        self.time          = ''         # 时间；
        self.trade_date    = ''         # 交易日期
