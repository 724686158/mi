#  -*- coding: utf-8 -*-
import redis
filename = "all_spiders.txt"
r = redis.Redis('122.114.62.116', 7001, 13)
keys = r.keys()
with open(filename, 'w') as f:
    f.write("")
for key in keys:
    with open(filename, 'a') as f:
        print key
        f.write((key + '\n').encode('utf8'))
        f.write((r.get(key) + '\n').encode('utf8'))