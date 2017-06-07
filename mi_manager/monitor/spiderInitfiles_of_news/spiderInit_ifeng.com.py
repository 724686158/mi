# -*- coding: utf-8 -*-
import redis
def init():
    print "pushing ifeng.com:start_url......"
    try:
        r = redis.Redis("192.168.139.239", 7001, 0)
        r.delete("ifeng.com:start_urls")
        r.delete("ifeng.com:dupefilter" + "0")
        r.delete("ifeng.com:requests")
        r.lpush("ifeng.com:start_urls", 'http://www.ifeng.com/')
        r2 = redis.Redis("192.168.139.239", 7001, 15)
        for keyname in 'downloader/request_count', 'downloader/response_count', 'downloader/response_status_count/200', 'item_scraped_count':
            r2.delete(keyname + "_" + "ifeng.com")
        print "pushing ifeng.com:start_url success"
    except Exception:
        print "pushing ifeng.com:start_url failed"
if __name__ == '__main__':
    init()
