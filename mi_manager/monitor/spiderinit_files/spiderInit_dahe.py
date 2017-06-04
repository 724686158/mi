# -*- coding: utf-8 -*-
import redis
def init():
    print "pushing dahe:start_url......"
    try:
        r = redis.Redis("192.168.139.239", 7001, 0)
        r.delete("dahe:start_urls")
        r.delete("dahe:dupefilter" + "0")
        r.delete("dahe:requests")
        r.lpush("dahe:start_urls", 'http://www.dahe.cn')
        r2 = redis.Redis("192.168.139.239", 7001, 15)
        for keyname in 'downloader/request_count', 'downloader/response_count', 'downloader/response_status_count/200', 'item_scraped_count':
            r2.delete(keyname + "_" + "dahe")
        print "pushing dahe:start_url success"
    except Exception:
        print "pushing dahe:start_url failed"
if __name__ == '__main__':
    init()
