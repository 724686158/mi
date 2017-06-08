#  -*- coding: utf-8 -*-
import pymongo
import mi.settings as settings
connection = pymongo.MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
db = connection[settings.MONGO_DATABASE]
table = db[settings.MONGO_COLLECTION_NAME + '_' + 'DomTreeItem']
con = 0
print type(table.find())
for item in table.find():
    try:

        print "Number:" , con
        print item['articleUrl']
        con = con + 1
    except Exception:
        print "exception"
