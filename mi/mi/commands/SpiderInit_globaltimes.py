# -*- coding: utf-8 -*-
import redis
import mi.settings as prime_settings
def init():
    print "pushing globaltimes:start_url......"
    try:
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT)
        r.delete("globaltimes:start_urls")
        r.delete("globaltimes:dupefilter" + "0")
        r.delete("globaltimes:requests")
        r.lpush("globaltimes:start_urls", 'http://www.un.org/chinese/News')
        print "pushing globaltimes:start_url success"
    except Exception:
        print "pushing globaltimes:start_url failed"
if __name__ == '__main__':
    init()
