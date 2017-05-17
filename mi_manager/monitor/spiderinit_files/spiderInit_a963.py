# -*- coding: utf-8 -*-
import redis
def init():
    print "pushing a963:start_url......"
    try:
        r = redis.Redis("192.168.139.239", 7001, 0)
        r.delete("a963:start_urls")
        r.delete("a963:dupefilter" + "0")
        r.delete("a963:requests")
        r.lpush("a963:start_urls", 'http://www.a963.com')
        r2 = redis.Redis("192.168.139.239", 7001, 15)
        for keyname in 'downloader/request_count', 'downloader/response_count', 'downloader/response_status_count/200', 'item_scraped_count':
            r2.delete(keyname + "_" + "a963")
        print "pushing a963:start_url success"
    except Exception:
        print "pushing a963:start_url failed"
if __name__ == '__main__':
    init()
