#  -*- coding: utf-8 -*-
import redis
import settings as settings
r = redis.Redis(settings.REDIS_HOST, 6379, db=settings.SPIDERS_DB)
keys = r.keys()
filename = "spiders.txt"
with open(filename, 'r') as f:
    key = f.readline()
    con = 0
    while key.__len__() > 0:
        con = con + 1
        print con
        key = key.split('\n')[0]
        print key
        info = f.readline().split('\n')[0]
        print info
        r.set(key, info)
        key = f.readline()
        if key.__len__() < 2:
            key = f.readline()


