# -*- coding: utf-8 -*-
from mysqlHelper import MysqlHelper
import mi.settings as prime_settings

class MysqlInit():
    def __init__(self):
        self.dbHelper = MysqlHelper()
        self.sql_createtable = prime_settings.sql_createtable

    def start(self):
        #新建数据库
        print "尝试创建mysql数据库"
        try:
            self.dbHelper.createDatabase()
        except Exception:
            print "创建mysql数据库失败"

        #新建表
        print "尝试创建mysql数据表"
        try:
            self.dbHelper.createTable(self.sql_createtable)
        except Exception:
            print "创建mysql数据表失败"