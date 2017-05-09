# -*- coding: utf-8 -*-
import redis
import mi.settings as prime_settings
def init():
    print "pushing wallstreetcn:start_url......"
    try:
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT)
        r.delete("wallstreetcn:start_urls")
        r.delete("wallstreetcn:dupefilter" + "0")
        r.delete("wallstreetcn:requests")
        r.lpush("wallstreetcn:start_urls", 'https://wallstreetcn.com')
        print "pushing wallstreetcn:start_url success"
    except Exception:
        print "pushing wallstreetcn:start_url failed"
if __name__ == '__main__':
    init()
