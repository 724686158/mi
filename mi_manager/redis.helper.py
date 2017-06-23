# -*- encoding: utf-8 -*-
import redis
import settings
r = redis.Redis(settings.CORE_REDIS_HOST, settings.CORE_REDIS_PORT, settings.RUNNINGDATA_DB)
print r.lrange('taobao:item_types', 0, -1)
types =  r.lrange('taobao:item_types', 0, -1)
for type in types:
    print type
r = redis.Redis(settings.CORE_REDIS_HOST, settings.CORE_REDIS_PORT, settings.MONITOR_DB)
r.flushdb()