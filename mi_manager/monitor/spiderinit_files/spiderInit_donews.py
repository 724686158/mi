# -*- coding: utf-8 -*-
import redis
def init():
    print "pushing donews:start_url......"
    try:
        r = redis.Redis("192.168.139.239", 7001, 0)
        r.delete("donews:start_urls")
        r.delete("donews:dupefilter" + "0")
        r.delete("donews:requests")
        r.lpush("donews:start_urls", 'http://www.donews.com')
        r2 = redis.Redis("192.168.139.239", 7001, 15)
        for keyname in 'downloader/request_count', 'downloader/response_count', 'downloader/response_status_count/200', 'item_scraped_count':
            r2.delete(keyname + "_" + "donews")
        print "pushing donews:start_url success"
    except Exception:
        print "pushing donews:start_url failed"
if __name__ == '__main__':
    init()
