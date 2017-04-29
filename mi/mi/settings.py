# -*- coding: utf-8 -*-

BOT_NAME = 'mi'

SPIDER_MODULES = ['mi.spiders']
NEWSPIDER_MODULE = 'mi.spiders'

#配置
ROBOTSTXT_OBEY = False   #是否启用robots
COOKIES_ENABLED = False  #禁止COOKIES
RETRY_ENABLED = False   #禁止重试
DOWNLOAD_TIMEOUT = 30   #超时时限
DOWNLOAD_DELAY = 0.5   #间隔时间
CONCURRENT_REQUESTS_PER_DOMAIN = 20 #对单个域名最大并发量
#DEPTH_LIMIT = 20 #爬取深度,20是为了避免那些动态生成链接的网站造成的死循环,暂时没遇到这种网站,先禁用了

# redis —— url存储
REDIS_HOST = '192.168.139.239'
REDIS_PORT = 7001
# redis —— 去重队列
FILTER_HOST = '192.168.139.239'
FILTER_PORT = 7001
FILTER_DB = 0
# redis ——用于监控的数据库
FLASK_DB = 0
#存储爬虫运行数据的四个队列,需要与monitor.monitor_settings中的一致
request_count = 'downloader/request_count'
response_count = 'downloader/response_count'
response_status200_count = 'downloader/response_status_count/200'
item_scraped_count = 'item_scraped_count'
STATS_KEYS = ["downloader/request_count", "downloader/response_count", "downloader/response_status_count/200", "item_scraped_count"]

# mongodb数据库的配置信息
MONGO_URI = 'mongodb://192.168.139.239:27017'
MONGO_DATABASE = 'mi'
MONGO_COLLECTION_NAME = "data_20170417_0"

#监控服务器信息
MONITOR_HOST = "0.0.0.0"
MONITOR_PORT = "5020"

#Mysql数据库的配置信息
MYSQL_HOST = "192.168.139.239"
MYSQL_PORT = 3306
MYSQL_DBNAME = 'data_20170417_0'    #数据库名字
MYSQL_USER = 'root'                 #数据库账号
MYSQL_PASSWD = 'mi'                 #数据库密码

#用于创建电商相关的表
sql_createtable = "create table ECommerce(eCommerceId int primary key auto_increment, eCommerceName varchar(100), eCommerceUrl varchar(200)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin; \
create table ECommerceShop(shopId int primary key auto_increment, eCommerceId int, shopName varchar(100), shopUrl varchar(200), shopLocation varchar(100), shopPhoneNumber varchar(100), FOREIGN KEY (eCommerceId) REFERENCES ECommerce(eCommerceId)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin auto_increment=1; \
create table ECommerceShopComment(shopId int primary key, shopTotalRating varchar(50), shopTotalRatingCTC varchar(50), shopGoodQualitySatisficationRating varchar(50), shopGoodQualitySatisficationRatingCTC varchar(50), shopServiceSatisficationRating varchar(50), shopServiceSatisficationRatingCTC varchar(50), shopLogisticsSpeedSatisficationRating varchar(50), shopLogisticsSpeedSatisficationRatingCTC varchar(50), shopGoodDescriptionSatisficationRating varchar(50), shopGoodDescriptionSatisficationRatingCTC varchar(50), shopProcessingReturnAndExchangeGoodSatisficationRating varchar(50), shopProcessingReturnAndExchangeGoodSatisficationRatingCTC varchar(50), shopDisobeyRulesTimes int, FOREIGN KEY (shopId) REFERENCES ECommerceShop(shopId)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin; \
create table ECommerceGood(goodId int primary key auto_increment, shopId int, goodName varchar(100), goodUrl varchar(200), goodPrice float, FOREIGN KEY (shopId) REFERENCES ECommerceShop(shopId)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin auto_increment=1; \
create table ECommerceGoodComment(goodId int primary key, goodCommentsCount int, goodCommentsUrl varchar(200), goodDisplayPictureCount int, goodAddCommentCount int, goodRankBetterCommentCount int, goodRankMediateCommentCount int, goodRankWorseCommentCount int, FOREIGN KEY (goodId) REFERENCES ECommerceGood(goodId)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin; \
"

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
    'mi.middlewares.middleware_proxy.RandomProxyMiddleware':400,# 代理相关
    'mi.middlewares.middleware_rotateUserAgent.RotateUserAgentMiddleware': 401,
    'mi.middlewares.middleware_monitor.StatcollectorMiddleware': 402,# 可视化相关
}

# 代理相关参数
# 存储可信代理的文件路径
HTTPPROXY_FILE_PATH = "/home/solitarius/mi/mi/mi/proxy/valid_proxy.txt"
# 请求连接失败重试次数
RETRY_TIMES = 6
# proxy失败重试次数
PROXY_USED_TIMES = 2
# 重试返回码
RETRY_HTTP_CODES = [500, 503, 504, 599, 403]
# 下载超时
DOWNLOAD_TIMEOUT = 6

SCHEDULER = "mi.scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'mi.scrapy_redis.queue.SpiderPriorityQueue'

#自定义命令
COMMANDS_MODULE = 'mi.commands'

#没有这个会出现异常
DOWNLOAD_HANDLERS = {'s3': None,}