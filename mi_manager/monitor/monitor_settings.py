# -*- coding: utf-8 -*-
TIMEINTERVAL = 500#监控台刷新时间间隔，单位毫秒
POINTINTERVAL = 50#图上各点之间间隔，越小则表示点越密集
POINTLENGTH = 5000#图上点的数量，越大则表示图上时间跨度越长

#存储爬虫运行数据的四个队列,名字不可更改
request_count = "downloader/request_count"
response_count = "downloader/response_count"
response_status200_count = "downloader/response_status_count/200"
item_scraped_count = "item_scraped_count"

STATS_KEYS = ["downloader/request_count", "downloader/response_count", "downloader/response_status_count/200", "item_scraped_count"]
REDIS_HOST = "192.168.139.239"
REDIS_PORT = 7001
REDIS_DB = 0
APP_HOST = "0.0.0.0"
APP_PORT = 5020