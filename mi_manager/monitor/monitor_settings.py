# -*- coding: utf-8 -*-
TIMEINTERVAL = 500#监控台刷新时间间隔，单位毫秒
POINTINTERVAL = 5#图上各点之间间隔，越小则表示点越密集
POINTLENGTH = 10000#图上点的数量，越大则表示图上时间跨度越长

#存储爬虫运行数据的四个队列,名字不可更改
STATS_KEYS = ['downloader/request_count', 'downloader/response_count', 'downloader/response_status_count/200', 'item_scraped_count']
REDIS_HOST = '192.168.139.239'
REDIS_PORT = 7001

APP_HOST = '192.168.139.239'
APP_PORT = 5020

# 用于存储调度队列 ———— 的redis数据据库编号（0～15）
FILTER_DB = 0

# 用于暂存爬虫运行时数据 ———— 的redis数据据库编号（0～15）
RUNNINGDATA_DB = 11

# 用于存储Cookie数据 ———— 的redis数据据库编号（0～15）
COOKIES_DB = 12

# 用于存储新闻类爬虫配置参数 ———— 的redis数据据库编号（0～15）
SPIDERS_DB = 13

# 用于存储任务信息 ———— 的redis数据据库编号（0～15）
MISSIONS_DB = 14

# 用于存储Monitor数据 ———— 的redis数据据库编号（0～15）
MONITOR_DB = 15

