# -*- coding: utf-8 -*-
import redis
import mi.settings as prime_settings
def init():
    print "pushing huxiu:start_url......"
    try:
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT)
        r.delete("huxiu:start_urls")
        r.delete("huxiu:dupefilter" + "0")
        r.delete("huxiu:requests")
        r.lpush("huxiu:start_urls", 'https://www.huxiu.com')
        print "pushing huxiu:start_url success"
    except Exception:
        print "pushing huxiu:start_url failed"
if __name__ == '__main__':
    init()
