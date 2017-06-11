#  -*- coding: utf-8 -*-
import redis
import settings as settings
filename = "all_spiders.txt"
r = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, db=settings.SPIDERS_DB)
keys = r.keys()
with open(filename, 'w') as f:
    f.write("")
for key in keys:
    with open(filename, 'a') as f:
        print key
        f.write((key + '\n').encode('utf8'))
        f.write((r.get(key) + '\n').encode('utf8'))