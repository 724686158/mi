# -*- coding: utf-8 -*-
import pymysql
import mi.settings as prime_settings

class MysqlInit():
    def __init__(self):
        self.dbHelper = DBHelper()
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



class DBHelper():
    def __init__(self):
        self.host = prime_settings.MYSQL_HOST
        self.port = prime_settings.MYSQL_PORT
        self.user = prime_settings.MYSQL_USER
        self.passwd = prime_settings.MYSQL_PASSWD
        self.db = prime_settings.MYSQL_DBNAME

    def connectMysql(self):
        conn = pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               passwd=self.passwd,
                               charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)
        return conn

    def connectDatabase(self):
        conn = pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               passwd=self.passwd,
                               db=self.db,
                               charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)
        return conn

    def createDatabase(self):
        conn = self.connectMysql()

        sql = "create database if not exists " + self.db
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()

    def createTable(self, sql):
        conn = self.connectDatabase()

        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()

    def insert(self, sql, *params):
        conn = self.connectDatabase()

        cur = conn.cursor();
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()

    def update(self, sql, *params):
        conn = self.connectDatabase()

        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()

    def delete(self, sql, *params):
        conn = self.connectDatabase()
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()