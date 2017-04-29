# -*- coding: utf-8 -*-
import redis
import mi.settings as prime_settings
def init():
    print "pushing aaa_start_url......"
    try:
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT)
        r.delete("aaa_start_urls")
        r.delete("aaa_dupefilter" + "0")
        r.delete("aaa_requests")
        r.lpush("aaa_start_urls", 'aaa')
        print "pushing aaa_start_url success"
    except Exception:
        print "pushing aaa_start_url failed"
if __name__ == '__main__':
    init()
