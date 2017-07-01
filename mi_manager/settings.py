# -*- coding: utf-8 -*-
# marathon的地址 (请确保zookeeper+mesos+marathon框架正常运行)
MESOS_URL = 'http://122.114.62.116:5050'
MARATHON_URL = 'http://122.114.62.116:18082'

# 核心redis数据库
# 地址
CORE_REDIS_HOST = '122.114.62.116'
# 端口
CORE_REDIS_PORT = 7001
# 可用内存 (单位G, 建议1G以上)
CORE_REDIS_MAX_MEMORY = 2


# mi_manager web前端的地址及端口
APP_HOST = '122.114.62.116'
APP_PORT = 5020

# 监控模块的相对路径
MONITOR_TEMP_PATH = '/monitor'

# 监控模块的相对路径
DAEMON_TEMP_PATH = '/daemon'

# 已知的可处理的电商名单

##############################################################################################
# redis 数据库分布
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