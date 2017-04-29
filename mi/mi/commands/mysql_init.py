# -*- coding: utf-8 -*-
from mysqlHelper import MysqlHelper
import mi.settings as prime_settings

class MysqlInit():
    def __init__(self):
        self.dbHelper = MysqlHelper()
        self.sql_createtable = prime_settings.sql_createtable

    def start(self):
        #新建数据库
        print "trying to create database"
        try:
            self.dbHelper.createDatabase()
        except Exception:
            print "create database with problem"

        #新建表
        print "trying to create table"
        try:
            self.dbHelper.createTable(self.sql_createtable)
        except Exception:
            print "create table with problem"