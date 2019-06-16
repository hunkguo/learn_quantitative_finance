# encoding: UTF-8
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
