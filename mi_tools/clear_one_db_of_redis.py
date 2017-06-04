#  -*- coding: utf-8 -*-
import redis
import settings as settings
r = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, db=settings.MONITOR_DB)
r.flushdb()