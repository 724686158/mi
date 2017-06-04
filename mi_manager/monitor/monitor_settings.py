# -*- coding: utf-8 -*-
TIMEINTERVAL = 500#监控台刷新时间间隔，单位毫秒
POINTINTERVAL = 5#图上各点之间间隔，越小则表示点越密集
POINTLENGTH = 10000#图上点的数量，越大则表示图上时间跨度越长

#存储爬虫运行数据的四个队列,名字不可更改
STATS_KEYS = ['downloader/request_count', 'downloader/response_count', 'downloader/response_status_count/200', 'item_scraped_count']
REDIS_HOST = '192.168.139.239'
REDIS_PORT = 7001

APP_HOST = '192.168.210.152'
APP_PORT = 5020

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

# 临时路径,用于解决开发环境和生产环境中路径当前路径不一直的问题（开发环境中设为空）
#TEMP_PATH = '/monitor'
TEMP_PATH = ''

#Mysql数据库的配置信息
MYSQL_HOST = "192.168.139.239"
MYSQL_PORT = 3306
MYSQL_DBNAME = 'data_20170531_0'    #数据库名字
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
