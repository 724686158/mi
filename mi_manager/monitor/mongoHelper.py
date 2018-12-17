# -*- coding: utf-8 -*-
import redis
import pymongo
import settings as prime_settings

class MongoHelper():

    def connectMongo(self, host, port):
        conn = pymongo.MongoClient(host, port)
        return conn

    def connectDatabase(self, host, port, dbname):
        conn = self.connectMongo(host, port)
        db = conn[dbname]
        return db

    def discovery_and_connectDatabase_for_mission(self, mission_name):
        try:
            r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, prime_settings.MISSION_DB)
            mongo_dbname = eval(r.get(mission_name))['resource_dic']['mongo']
            r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, prime_settings.RESOURCES_MONGO_DB)
            mysql_detail = r.get(mongo_dbname)
            dic = eval(mysql_detail)
            conn = self.connectMongo(dic['host'], int(dic['post']))
            db = conn[mission_name]
            return db
        except:
            print '无法连接到任务[' + mission_name + ']所使用的Mongo数据库'
