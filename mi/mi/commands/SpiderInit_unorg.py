# -*- coding: utf-8 -*-
import redis
import mi.settings as prime_settings
def init():
    print "pushing SpiderInit_unorg.py:start_url......"
    try:
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT)
        r.delete("unorg:start_urls")
        r.delete("unorg:dupefilter" + "0")
        r.delete("unorg:requests")
        r.lpush("unorg:start_urls", 'https://www.architecturaldigest.in')
        print "pushing unorg:start_url success"
    except Exception:
        print "pushing unorg:start_url failed"
if __name__ == '__main__':
    init()
