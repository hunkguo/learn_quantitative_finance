# encoding: UTF-8

"""
定时服务，可无人值守运行，实现每日自动下载更新历史行情数据到数据库中。
"""

from DataService.tushareData import *
from datetime import datetime


if __name__ == '__main__':
    taskCompletedDate = None
    
    # 生成一个随机的任务下载时间，用于避免所有用户在同一时间访问数据服务器
    taskTime = datetime.now().replace(hour=17, minute=10, second=0)

    # 进入主循环
    while True:
        t = datetime.now()
        # 每天到达任务下载时间后，执行数据下载的操作
        if t.time() > taskTime.time() and (taskCompletedDate is None or t != taskCompletedDate):
            downloadAllStock()
            downloadTradeCalenday()
            if (taskCompletedDate is None):
                downloadTradeDataDaily(50)
            else:
                downloadTradeDataDaily(1)
            # 更新任务完成的日期
            taskCompletedDate = t.date()
        else:
            print(u'当前时间%s，任务定时%s' %(t, taskTime))

        sleep(60)
        #break
