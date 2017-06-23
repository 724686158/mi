# -*- coding: utf-8 -*-
import pymongo
import settings as prime_settings
class MongoHelper():
    def __init__(self):
        self.host = prime_settings.MONGO_HOST
        self.port = prime_settings.MONGO_PORT

    def connectMysql(self):
        conn = pymongo.MongoClient(self.host, self.port)
        return conn

    def connectDatabase(self, dbname = prime_settings.MONGO_DATABASE):
        conn = self.connectMysql()
        db = conn[dbname]
        return db