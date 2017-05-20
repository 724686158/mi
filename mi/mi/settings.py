# -*- coding: utf-8 -*-

BOT_NAME = 'mi'
SPIDER_MODULES = ['mi.spiders']
NEWSPIDER_MODULE = 'mi.spiders'

# scrapy基本属性配置
# 是否启用robots
ROBOTSTXT_OBEY = False
# 是否启用COOKIES
COOKIES_ENABLED = True
COOKIES_DEBUG = True
# 是否启用重试
RETRY_ENABLED = False
# 超时时限
DOWNLOAD_TIMEOUT = 30
# 间隔时间
DOWNLOAD_DELAY = 0.5
# 对单个域名最大并发量
CONCURRENT_REQUESTS_PER_DOMAIN = 20
#DEPTH_LIMIT = 20 #爬取深度,20是为了避免那些动态生成链接的网站造成的死循环,暂时没遇到这种网站,先禁用了

# redis —— url存储
REDIS_HOST = '192.168.139.239'
REDIS_PORT = 7001
# redis —— 去重队列
FILTER_HOST = '192.168.139.239'
FILTER_PORT = 7001

# 用于存储调度队列 ———— 的redis数据据库编号（0～15）
FILTER_DB = 0

# 用于存储代理ip ———— 的redis数据据库编号（0～15）
PROXY_DB = 10

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

#存储爬虫运行数据的四个队列,需要与monitor.monitor_settings中的一致
STATS_KEYS = ["downloader/request_count", "downloader/response_count", "downloader/response_status_count/200", "item_scraped_count"]

# mongodb数据库的配置信息
MONGO_HOST = '192.168.139.239'
MONGO_PORT = 27017
MONGO_DATABASE = 'mi'
MONGO_COLLECTION_NAME = 'data_20170510_0'

#监控服务器信息
MONITOR_HOST = "0.0.0.0"
MONITOR_PORT = "5020"

#Mysql数据库的配置信息
MYSQL_HOST = "192.168.139.239"
MYSQL_PORT = 3306
MYSQL_DBNAME = 'data_20170510_0'    #数据库名字
MYSQL_USER = 'root'                 #数据库账号
MYSQL_PASSWD = 'mi'                 #数据库密码

#用于创建电商相关的表
sql_createtable = '\
create table ECommerce(eCommerceId int primary key, eCommerceName varchar(32), eCommerceUrl varchar(256)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin; \
create table ECommerceShop(eCommerceId int, shopId varchar(32), shopName varchar(256), shopUrl varchar(1024), shopLocation varchar(256), shopPhoneNumber varchar(256), PRIMARY KEY (eCommerceId, shopId), FOREIGN KEY (eCommerceId) REFERENCES ECommerce(eCommerceId)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin; \
create table ECommerceShopComment(eCommerceId int, shopId varchar(32), shopCommentsUrl varchar(256), shopCommentsData varchar(2048), PRIMARY KEY (eCommerceId, shopId), FOREIGN KEY (eCommerceId) REFERENCES ECommerce(eCommerceId)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin; \
create table ECommerceGood(eCommerceId int, goodId varchar(32), shopId varchar(32), goodName varchar(1024), goodUrl varchar(1024), goodPrice varchar(32), PRIMARY KEY (eCommerceId, goodId), FOREIGN KEY (eCommerceId) REFERENCES ECommerce(eCommerceId)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin; \
create table ECommerceGoodComment(eCommerceId int, goodId varchar(32), goodCommentsUrl varchar(256), goodCommentsData varchar(2048), PRIMARY KEY (eCommerceId, goodId), FOREIGN KEY (eCommerceId) REFERENCES ECommerce(eCommerceId)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin; \
'

#日志设置,禁用“LOG_STDOUT=True”
#LOG_FILE='mi.log'
#LOG_LEVEL='INFO'


#pipelines 从300累加
ITEM_PIPELINES = {
    'mi.pipelines.pipeline_mongo.MongoPipeline':300,
    'mi.pipelines.pipeline_mysql.MysqlPipeline':301,
    'mi.pipelines.pipeline_monitor.SpiderRunStatspipeline':302#可视化相关
}

# 中间件
# 注意不要使用'scrapy.downloadermiddlewares.retry.RetryMiddleware'，此中间件会造成程序卡死
DOWNLOADER_MIDDLEWARES = {
    #'mi.middlewares.middleware_proxy.RandomProxyMiddleware':400,# 代理相关
    'mi.middlewares.middleware_rotateUserAgent.RotateUserAgentMiddleware': 401,
    'mi.middlewares.middleware_monitor.StatcollectorMiddleware': 402,# 可视化相关
    'mi.middlewares.middleware_cookie.CookieMiddleware': 700,# 该中间件将重试可能由于临时的问题，例如连接超时或者HTTP 500错误导致失败的页面。尝试加上cookie重新访问
}

# 请求连接失败重试次数
RETRY_TIMES = 6
# proxy失败重试次数
PROXY_USED_TIMES = 2
# 重试返回码
RETRY_HTTP_CODES = [500, 503, 504, 599, 403, 302]
# 下载超时
DOWNLOAD_TIMEOUT = 6

SCHEDULER = 'mi.scrapy_redis.scheduler.Scheduler'
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'mi.scrapy_redis.queue.SpiderPriorityQueue'

#自定义命令
COMMANDS_MODULE = 'mi.commands'

#没有这个会出现异常
DOWNLOAD_HANDLERS = {'s3': None,}