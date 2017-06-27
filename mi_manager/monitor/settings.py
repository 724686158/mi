# -*- coding: utf-8 -*-
# mi_manager
APP_HOST = '192.168.210.29'
APP_PORT = 5020
# 核心redis服务器
REDIS_HOST = '122.114.62.116'
REDIS_PORT = 7001

# mysql数据库的配置信息(实现资源读取之后删除)
MYSQL_HOST = '122.114.62.116'
MYSQL_PORT = 3306
MYSQL_DBNAME = 'data_20170612_01'    #数据库名字
MYSQL_USER = 'root'                 #数据库账号
MYSQL_PASSWD = 'mi'                 #数据库密码
# mongodb数据库的配置信息(实现资源读取之后删除)
MONGO_HOST = '122.114.62.116'
MONGO_PORT = 27017
MONGO_DATABASE = 'data_20170612_01'

# 监控器相关参数
TIMEINTERVAL = 2000#监控台刷新时间间隔，单位毫秒
POINTINTERVAL = 10#图上各点之间间隔，越小则表示点越密集
POINTLENGTH = 2000#图上点的数量，越大则表示图上时间跨度越长
# 存储爬虫运行数据的四个队列
STATS_KEYS = ['downloader/request_count', 'downloader/response_count', 'downloader/response_status_count/200', 'item_scraped_count']

##############################################################################################
# 用于存储调度队列 ———— 的redis数据据库编号（0～15）
FILTER_DB = 0

# 用于存储记号变量 ———— 的redis数据据库编号（0～15）
SYMBOL_DB = 1

# 用于存储task(带处理, 已处理) ———— 的redis数据据库编号（0～15）
TASK_DB = 2

# 用于进行task调度的有序集合 ———— 的redis数据据库编号（0～15）
DISPATCH_DB = 3

# 用于存储主任务 ———— 的redis数据据库编号（0～15）
MISSION_DB = 4

# 用于存储子任务 ———— 的redis数据据库编号（0～15）
SUBMISSION_DB = 5

# 用于存储爬虫配置信息 ———— 的redis数据据库编号（0～15）
SETTINGS_DB = 6

# 用于存储資源(REDIS服务器)的信息 ———— 的redis数据据库编号（0～15）
RESOURCES_REDIS_DB = 7

# 用于存储資源(MYSQL服务器)的信息 ———— 的redis数据据库编号（0～15）
RESOURCES_MYSQL_DB = 8

# 用于存储資源(MONGO服务器)的信息 ———— 的redis数据据库编号（0～15）
RESOURCES_MONGO_DB = 9

# 用于存储代理ip ———— 的redis数据据库编号（0～15）
PROXY_DB = 10

# 用于暂存爬虫运行时数据 ———— 的redis数据据库编号（0～15）
RUNNINGDATA_DB = 11

# 用于存储Cookie数据 ———— 的redis数据据库编号（0～15）
COOKIES_DB = 12

# 用于存储新闻类爬虫配置参数 ———— 的redis数据据库编号（0～15）
SPIDERS_DB = 13

# 用于分类爬虫(共三个类别： Whitelist, Fuzzy, Ecommerce) ———— 的redis数据据库编号（0～15）
CLASSIFIER_DB = 14

# 用于存储Monitor数据 ———— 的redis数据据库编号（0～15）
MONITOR_DB = 15
##############################################################################################

# 临时路径,用于解决开发环境和生产环境中路径当前路径不一直的问题（开发环境中设为空）
TEMP_PATH = '/monitor'