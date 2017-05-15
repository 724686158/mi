#  -*- coding: utf-8 -*-
import redis
import mi.settings as settings
r = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, db=settings.FILTER_DB)
keys = r.keys()

filename = "all_requests.txt"
with open(filename, 'w') as f:
    f.write("")

for key in keys:
    if "requests" in key:
        with open(filename, 'a') as f:
            list = r.zrange(key, 0, -1)
            for req in list:
                f.write((req + '\n'))