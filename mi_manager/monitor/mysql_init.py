# -*- coding: utf-8 -*-
from mysqlHelper import MysqlHelper

import settings as prime_settings

#用于创建电商相关的表
sql_createtable = '\
CREATE TABLE IF NOT EXISTS ECommerce(eCommerceName varchar(16) primary key, eCommerceUrl varchar(512)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin; \
CREATE TABLE IF NOT EXISTS ECommerceShop(eCommerceName varchar(16), shopId varchar(32), shopName varchar(1024), shopUrl varchar(1024), shopLocation varchar(256), shopPhoneNumber varchar(256), updateTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (eCommerceName, shopId), FOREIGN KEY (eCommerceName) REFERENCES ECommerce(eCommerceName)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin; \
CREATE TABLE IF NOT EXISTS ECommerceShopComment(eCommerceName varchar(16), shopId varchar(32), shopCommentsUrl varchar(1024), shopCommentsData varchar(2048), updateTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (eCommerceName, shopId), FOREIGN KEY (eCommerceName) REFERENCES ECommerce(eCommerceName)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin; \
CREATE TABLE IF NOT EXISTS ECommerceGood(eCommerceName varchar(16), goodId varchar(32), shopId varchar(32), goodName varchar(1024), goodUrl varchar(1024), goodPrice varchar(32), updateTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (eCommerceName, goodId), FOREIGN KEY (eCommerceName) REFERENCES ECommerce(eCommerceName)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin; \
CREATE TABLE IF NOT EXISTS ECommerceGoodComment(eCommerceName varchar(16), goodId varchar(32), goodCommentsUrl varchar(1024), goodCommentsData varchar(2048), updateTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (eCommerceName, goodId), FOREIGN KEY (eCommerceName) REFERENCES ECommerce(eCommerceName)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin; \
'

class MysqlInit():
    def __init__(self):
        self.dbHelper = MysqlHelper()

    def start(self):
        #新建数据库
        print "尝试创建mysql数据库"
        try:
            self.dbHelper.createDatabase()
            print "创建mysql数据库成功"
        except Exception:
            print "创建mysql数据库失败"

        #新建表
        print "尝试创建mysql数据表"
        try:
            self.dbHelper.createTable(sql_createtable)
            print "创建mysql数据表成功"
        except Exception:
            print "创建mysql数据表失败"