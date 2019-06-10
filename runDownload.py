# encoding: UTF-8

from DataService.tushareData import *


if __name__ == '__main__':
    downloadAllStock()
    downloadTradeCalenday()
    downloadTradeDataDaily()