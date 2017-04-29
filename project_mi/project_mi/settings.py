# -*- coding: utf-8 -*-

BOT_NAME = 'project_mi'

SPIDER_MODULES = ['project_mi.spiders']
NEWSPIDER_MODULE = 'project_mi.spiders'


#配置
COOKIES_ENABLED = False  #禁止COOKIES
RETRY_ENABLED = False   #禁止重试
DOWNLOAD_TIMEOUT = 15   #超时时限
DOWNLOAD_DELAY = 0.5   #间隔时间

# 数据库设置
# mongodb
MONGO_URI = 'mongodb://192.168.139.219:27017'
MONGO_DATABASE = 'mi'
MONGO_COLLECTION_NAME = "date_20170402"
# redis —— url存储
REDIS_HOST = '192.168.139.219'
REDIS_PORT = 7001
REDIE_URL = None
# redis —— 去重队列
FILTER_URL = None
FILTER_HOST = '192.168.139.219'
FILTER_PORT = 7001
FILTER_DB = 0


#改变user-agent头
DOWNLOADER_MIDDLEWARES = {
    'project_mi.rotateUserAgentMiddleware.RotateUserAgentMiddleware': 400,
}

ITEM_PIPELINES = {
    'project_mi.pipelines.ArticlePipeline': 300,
}

#调度模块
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

#没有这个会出现异常
DOWNLOAD_HANDLERS = {'s3': None,}