# -*- coding: utf-8 -*-
import redis
import pymysql
import settings as prime_settings
class MysqlHelper():
    # 连接Mysql
    def connectMysql(self, host = prime_settings.MYSQL_HOST, port = prime_settings.MYSQL_PORT, user = prime_settings.MYSQL_USER, passwd = prime_settings.MYSQL_PASSWD):
        conn = pymysql.connect(host,
                               port,
                               user,
                               passwd,
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


    # 创建数据库
    def createDatabase_for_mission(self, mission_name):
        conn = self.discovery_and_connect_for_mission(mission_name)
        sql = "create database if not exists " + mission_name
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()

    # 创建数据表
    def createTable_for_mission(self, mission_name, sql):
        conn = self.discovery_and_connectDatabase_for_mission(mission_name)
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()

    def insert_for_mission(self, mission_name, sql, *params):
        conn = self.discovery_and_connectDatabase_for_mission(mission_name)
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()

    def delete_for_mission(self, mission_name, sql, *params):
        conn = self.discovery_and_connectDatabase_for_mission(mission_name)
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()

    def update_for_mission(self, mission_name, sql, *params):
        conn = self.discovery_and_connectDatabase_for_mission(mission_name)
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()

    def select_for_mission(self, mission_name, sql):
        conn = self.discovery_and_connectDatabase_for_mission(mission_name)
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return result

    def discovery_and_connect_for_mission(self, mission_name):
        try:
            r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, prime_settings.MISSION_DB)
            mysql_dbname = eval(r.get(mission_name))['resource_dic']['mysql']
            r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, prime_settings.RESOURCES_MYSQL_DB)
            mysql_detail = r.get(mysql_dbname)
            dic = eval(mysql_detail)
            conn = pymysql.connect(host=dic['host'], port=int(dic['post']), user=dic['user'], passwd=dic['password'],
                                   charset='utf8', cursorclass=pymysql.cursors.DictCursor)
            return conn
        except:
            print '无法连接到任务[' + mission_name + ']所使用的Mysql资源'


    def discovery_and_connectDatabase_for_mission(self, mission_name):
        try:
            r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, prime_settings.MISSION_DB)
            mysql_dbname = eval(r.get(mission_name))['resource_dic']['mysql']
            r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, prime_settings.RESOURCES_MYSQL_DB)
            mysql_detail = r.get(mysql_dbname)
            dic = eval(mysql_detail)
            conn = pymysql.connect(host=dic['host'],
                                   port=int(dic['post']),
                                   user=dic['user'],
                                   passwd=dic['password'],
                                   db=mission_name,
                                   charset='utf8',
                                   cursorclass=pymysql.cursors.DictCursor)
            return conn
        except:
            print '无法连接到任务[' + mission_name + ']所使用的Mysql数据库'

