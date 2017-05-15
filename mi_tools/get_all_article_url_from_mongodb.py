#  -*- coding: utf-8 -*-
import pymongo
import mi.settings as settings
connection = pymongo.MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
db = connection[settings.MONGO_DATABASE]
print db.collection_names()
filename = "articles_urls.txt"
with open(filename, 'w') as f:
    f.write("")
items = db[settings.MONGO_COLLECTION_NAME + '_' + 'ArticleItem']
con = 0
for item in items.find():
    try:
        print "Number:" , con
        print item['articleUrl']
        con = con + 1
        with open(filename, 'a') as f:
            f.write(item['articleUrl'] + '\n')
    except Exception:
        print "exception"