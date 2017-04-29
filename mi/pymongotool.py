#  -*- coding: utf-8 -*-
import pymongo
import mi.settings as settings
connection = pymongo.MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
db = connection[settings.MONGO_DATABASE]
print db.collection_names()
users = db[settings.MONGO_COLLECTION_NAME + '_' + 'DomTreeItem']
con = 0
for item in users.find():
    try:

        print "Number:" , con
        print item['url']
        con = con + 1
    except Exception:
        print "exception"
