#  -*- coding: utf-8 -*-
import pymongo
import mi.settings as settings
connection = pymongo.MongoClient(settings.MONGO_URI)
#f = open("./data.txt", 'w')
db = connection[settings.MONGO_DATABASE]
print db.collection_names()
users = db[settings.MONGO_COLLECTION_NAME]
con = 0
'''
    # 文章标题
    articleTitle = scrapy.Field()
    # 文章url
    articleUrl = scrapy.Field()
    # 文章内容
    articleContent = scrapy.Field()
    # 文章关键词1
    articleFirstTag = scrapy.Field()
    # 文章关键词2
    articleSecondTag = scrapy.Field()
    # 文章关键词3
    articleThirdTag = scrapy.Field()
'''
for item in users.find():
    try:

        print "Number:" , con
        print item['articleTitle']
        print item['articleUrl']
        print item['articleContent']
        print item['articleFirstTag']
        print item['articleSecondTag']
        print item['articleThirdTag']
        #print >> f, "Number:%d" % (con)
        #print >> f, "articleId:%s" % (item['articleId'])
        con = con + 1
    except Exception:
        print "exception"