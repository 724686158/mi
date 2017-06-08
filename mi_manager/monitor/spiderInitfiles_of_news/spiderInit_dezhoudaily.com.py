# -*- coding: utf-8 -*-
import redis
def init():
    print "pushing dezhoudaily.com:start_url......"
    try:
        r = redis.Redis("192.168.139.239", 7001, 0)
        r.delete("dezhoudaily.com:start_urls")
        r.delete("dezhoudaily.com:dupefilter" + "0")
        r.delete("dezhoudaily.com:requests")
        r.lpush("dezhoudaily.com:start_urls", 'http://www.dezhoudaily.com/news/dezhou/folder135/2017/06/2017-06-081288095.html')
        r2 = redis.Redis("192.168.139.239", 7001, 15)
        for keyname in 'downloader/request_count', 'downloader/response_count', 'downloader/response_status_count/200', 'item_scraped_count':
            r2.delete(keyname + "_" + "dezhoudaily.com")
        print "pushing dezhoudaily.com:start_url success"
    except Exception:
        print "pushing dezhoudaily.com:start_url failed"
if __name__ == '__main__':
    init()
