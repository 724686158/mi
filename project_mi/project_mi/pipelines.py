# -*- coding: utf-8 -*-

import pymongo
from project_mi.project_mi.settings import settings
class ArticlePipeline(object):

    def __init__(self):
        self.connection = pymongo.MongoClient(host='192.168.139.239', port=27017)
        self.db = self.connection['huxiu']
    def process_item(self, item, spider):
        articleDict={'id':item['articleId'],'content':item['content']}
        try:
            self.db['v'].insert(articleDict)
        except:
            self.db['article'].save(articleDict)

class ArticlePipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):

	# 集合名 使用之前会赋值
    collection_name = settings.MONGO_COLLECTION_NAME

	# 初始化该数据库
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod		# 指定该方法为类方法
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DATABASE','items')
        )

	# 数据库连接
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
	# 数据库关闭
    def close_spider(self,spider):
        self.client.close()

    # 将数据存入到数据库中
    def process_item(self,item,spider):
        if isinstance(item, ArticleItem):
            self.db[self.collection_name].insert(dict(item))           #存入数据库原始数据
        return item