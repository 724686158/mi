# -*- coding: utf-8 -*-
import redis
import mi.settings as prime_settings
def init():
    print "pushing baidunews_start_url......"
    try:
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT)
        r.delete("baidunews:start_urls")
        r.delete("baidunews:dupefilter" + "0")
        r.delete("baidunews:requests")
        r.lpush("baidunews:start_urls", 'http://news.baidu.com/')
        print "pushing baidunews_start_url success"
    except Exception:
        print "pushing baidunews_start_url failed"
if __name__ == '__main__':
    init()
