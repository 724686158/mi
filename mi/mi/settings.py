# -*- coding: utf-8 -*-
BOT_NAME = 'testmission12'
SUB_MISSION = 'huxiu.com'
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = True
RETRY_ENABLED = True
HTTP_PROXY_ENABLED = None
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 6
DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS_PER_DOMAIN = 10
DOWNLOAD_TIMEOUT = 10
REDIS_HOST = '122.114.62.116'
REDIS_PORT = 7001
FILTER_HOST = '122.114.62.116'
FILTER_PORT = 7001
MYSQL_HOST = '122.114.62.116'
MYSQL_PORT = 3306
MYSQL_DBNAME = 'testmission12'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'mi'
MONGO_HOST = '122.114.62.116'
MONGO_PORT = 27017
MONGO_DATABASE = 'testmission12'
COOKIES_DEBUG = True
AUTOTHROTTLE_DEBUG = True
SPIDER_MODULES = ['mi.spiders_of_eCommerce', 'mi.spiders_of_news_in_whiteList', 'mi.spiders_of_news_need_fuzzymatching']
##############################################################################################
FILTER_DB = 0
SYMBOL_DB = 1
TASK_DB = 2
DISPATCH_DB = 3
MISSION_DB = 4
SUBMISSION_DB = 5
SETTINGS_DB = 6
RESOURCES_REDIS_DB = 7
RESOURCES_MYSQL_DB = 8
RESOURCES_MONGO_DB = 9
PROXY_DB = 10
RUNNINGDATA_DB = 11
COOKIES_DB = 12
SPIDERS_DB = 13
CLASSIFIER_DB = 14
MONITOR_DB = 15
##############################################################################################
STATS_KEYS = ["downloader/request_count", "downloader/response_count", "downloader/response_status_count/200", "item_scraped_count"]
ITEM_PIPELINES = {
    'mi.pipelines.pipeline_mongo.MongoPipeline':300,
    'mi.pipelines.pipeline_mysql.MysqlPipeline':301,
}
DOWNLOADER_MIDDLEWARES = {
    'mi.middlewares.middleware_proxy.RandomProxyMiddleware':HTTP_PROXY_ENABLED,
    'mi.middlewares.middleware_rotateUserAgent.RotateUserAgentMiddleware': 401,
    'mi.middlewares.middleware_monitor.StatcollectorMiddleware': 402,
    'mi.middlewares.middleware_cookie.CookieMiddleware': None,
}
RETRY_TIMES = 6
PROXY_USED_TIMES = 2
RETRY_HTTP_CODES = [500, 503, 504, 599, 403]
SCHEDULER = 'mi.scrapy_redis.scheduler.Scheduler'
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'mi.scrapy_redis.queue.SpiderPriorityQueue'
DOWNLOAD_HANDLERS = {'s3': None,}