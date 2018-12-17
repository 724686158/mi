# -*- coding: utf-8 -*-
import redis
import pymysql
import settings as prime_settings


class MysqlHelper():
    # 创建数据库
    def createDatabase_for_mission(self, mission_name):
        conn = self.discovery_and_connect_for_mission(mission_name)
        sql = "CREATE DATABASE IF NOT EXISTS " + mission_name + " DEFAULT CHARSET=utf8 COLLATE=utf8_bin"
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
        except Exception:
            print '无法连接到任务[' + mission_name + ']所使用的Mysql资源' + Exception.message

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
        except Exception:
            print '无法连接到任务[' + mission_name + ']所使用的Mysql数据库' + Exception.message

