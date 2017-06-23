# -*- coding: utf-8 -*-
import pymysql
import settings as prime_settings
class MysqlHelper():
    def __init__(self):
        self.host = prime_settings.MYSQL_HOST
        self.port = prime_settings.MYSQL_PORT
        self.user = prime_settings.MYSQL_USER
        self.passwd = prime_settings.MYSQL_PASSWD
        self.db = prime_settings.MYSQL_DBNAME


    # 连接Mysql
    def connectMysql(self):
        conn = pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               passwd=self.passwd,
                               charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)
        return conn

    # 创建数据库
    def createDatabase(self, dbname = prime_settings.MYSQL_DBNAME):
        conn = self.connectMysql()
        sql = "create database if not exists " + dbname
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()


    # 连接数据库
    def connectDatabase(self, dbname = prime_settings.MYSQL_DBNAME):
        if dbname == prime_settings.MYSQL_DBNAME:
            host = self.host
            port = self.port
            user = self.user
            passwd = self.passwd
        else:
            pass #这里存在不支持远程数据库的bug

        conn = pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               passwd=self.passwd,
                               db= dbname,
                               charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)
        return conn

    # 创建数据表
    def createTable(self, sql):
        conn = self.connectDatabase()

        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()


    def insert(self, sql, *params):
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

    def update(self, sql, *params):
        conn = self.connectDatabase()
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()

    def select(self, sql):
        conn = self.connectDatabase()
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return result

    # 创建数据表
    def createTable_with_dbname(self, dbname, sql):
        conn = self.connectDatabase(dbname)

        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()

    def insert_with_dbname(self, dbname, sql, *params):
        conn = self.connectDatabase(dbname)
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()

    def delete_with_dbname(self, dbname, sql, *params):
        conn = self.connectDatabase(dbname)
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()

    def update_with_dbname(self, dbname, sql, *params):
        conn = self.connectDatabase(dbname)
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()

    def select_with_dbname(self, dbname, sql):
        conn = self.connectDatabase(dbname)
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return result