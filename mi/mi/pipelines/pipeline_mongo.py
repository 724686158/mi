# -*- coding: utf-8 -*-
import pymongo
from items import ArticleItem
import mi.settings as settings

class MongoPipeline(object):
    # 集合名 使用之前会赋值
    hp_collection_name = ''

    # 初始化该数据库
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod  # 指定该方法为类方法
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    # 数据库连接
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    # 数据库关闭
    def close_spider(self, spider):
        self.client.close()

    # 将数据存入到数据库中
    def process_item(self, item, spider):
        if isinstance(item, ArticleItem):
            self.hp_collection_name = settings.MONGO_COLLECTION_NAME
            self.db[self.hp_collection_name].insert(dict(item))  # 存入数据库原始数据
        return item