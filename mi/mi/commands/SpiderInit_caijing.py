# -*- coding: utf-8 -*-
import redis
import mi.settings as prime_settings
def init():
    print "pushing caijing_start_url......"
    try:
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT)
        r.delete("caijing_start_urls")
        r.delete("caijing_dupefilter" + "0")
        r.delete("caijing_requests")
        r.lpush("caijing_start_urls", 'http://www.caijing.com.cn')
        print "pushing caijing_start_url success"
    except Exception:
        print "pushing caijing_start_url failed"
if __name__ == '__main__':
    init()
