# -*- coding: utf-8 -*-
import pymongo
import settings as prime_settings
class MongoHelper():
    def __init__(self):
        self.host = prime_settings.MONGO_HOST
        self.port = prime_settings.MONGO_PORT
        self.db = prime_settings.MONGO_DATABASE

    def connectMysql(self):
        conn = pymongo.MongoClient(self.host, self.port)
        return conn

    def connectDatabase(self):
        conn = self.connectMysql()
        db = conn[self.db]
        return db
