#  -*- coding: utf-8 -*-
import redis
import settings as settings
r = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, db=settings.TASK_DB)
try:
    r.flushdb()
    r.rpush(2, 'jd');
    r.rpush(2, 'amazon')
    print 'rpush success'
except:
    print 'faild'