# -*- coding: utf-8 -*-
import pymysql
import mi.settings as prime_settings
class MysqlHelper():
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

        print sql
        print params
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