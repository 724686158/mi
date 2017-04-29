#  -*- coding: utf-8 -*-
import pymongo
import mi.settings as settings
connection = pymongo.MongoClient(settings.MONGO_URI)
f = open("./data.txt", 'w')
db = connection[settings.MONGO_DATABASE]
print db.collection_names()
users = db[settings.MONGO_COLLECTION_NAME]
con = 0
for item in users.find():
    try:
        print "Number:" , con
        print item['articleId']
        print item['articleTitle']
        print item['articleContent']
        print >> f, "Number:%d" % (con)
        print >> f, "articleId:%s" % (item['articleId'])
        con = con + 1
    except Exception:
        print "exception"