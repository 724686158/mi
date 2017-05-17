# -*- coding: utf-8 -*-
import redis
import mi.settings as prime_settings
def init():
    print "pushing aikan:start_url......"
    try:
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, prime_settings.FILTER_DB)
        r.delete("aikan:start_urls")
        r.delete("aikan:dupefilter" + "0")
        r.delete("aikan:requests")
        r.lpush("aikan:start_urls", 'http://aikanxinwen.com')
        print "pushing aikan:start_url success"
    except Exception:
        print "pushing aikan:start_url failed"
if __name__ == '__main__':
    init()
