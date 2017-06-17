# -*- coding: utf-8 -*-

# 尝试有序集合
import redis
import settings as prime_settings
r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, 2)
r.flushdb()
print r.zadd('www.baidu.com', "first_page", 5)
print r.zadd('www.baidu.com', "second_page", 2)
print r.zadd('www.baidu.com', "thirdd_page", 3)
print r.zadd('www.baidu.com', "third_page", 3)
print r.zadd('www.baidu.com', "thir_page", 3)
print r.zadd('www.baidu.com', "2_page", 2)
print r.zadd('www.baidu.com', "1_page", 1)
print r.zrevrange('www.baidu.com', 0, -1)