# -*- coding: utf-8 -*-
from mysqlHelper import MysqlHelper

# 用于创建电商相关的表
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

    def start(self, mission):
        # 新建数据库
        print "尝试创建mysql数据库"
        self.dbHelper.createDatabase_for_mission(mission)
        try:
            pass
            print "创建mysql数据库成功"
        except Exception:
            print "创建mysql数据库失败"
        # 新建表
        print "尝试创建mysql数据表"
        try:
            self.dbHelper.createTable_for_mission(mission, sql_createtable)
            print "创建mysql数据表成功"
        except Exception:
            print "创建mysql数据表失败"

        # 向数据表ECommerce中插入电商信息
        try:
            sql = "insert into ECommerce(eCommerceName, eCommerceUrl) values('amazon.cn', 'https://www.amazon.cn');".encode(encoding='utf-8')
            self.dbHelper.insert_for_mission(mission, sql)
            sql = "insert into ECommerce(eCommerceName, eCommerceUrl) values('dangdang.com', 'http://www.dangdang.com');".encode(encoding='utf-8')
            self.dbHelper.insert_for_mission(mission, sql)
            sql = "insert into ECommerce(eCommerceName, eCommerceUrl) values('gome.com.cn', 'http://www.gome.com.cn');".encode(encoding='utf-8')
            self.dbHelper.insert_for_mission(mission, sql)
            sql = "insert into ECommerce(eCommerceName, eCommerceUrl) values('jd.com', 'https://item.jd.com');".encode(encoding='utf-8')
            self.dbHelper.insert_for_mission(mission, sql)
            sql = "insert into ECommerce(eCommerceName, eCommerceUrl) values('taobao.com', 'https://www.taobao.com');".encode(encoding='utf-8')
            self.dbHelper.insert_for_mission(mission, sql)
            print "插入数据成功"
        except Exception:
            print "插入数据失败"