# -*- coding: utf-8 -*-
import redis
def init():
    print "pushing huxiu:start_url......"
    try:
        r = redis.Redis("192.168.139.239", 7001, 0)
        r.delete("huxiu:start_urls")
        r.delete("huxiu:dupefilter" + "0")
        r.delete("huxiu:requests")
        r.lpush("huxiu:start_urls", 'https://www.huxiu.com')
        r2 = redis.Redis("192.168.139.239", 7001, 15)
        for keyname in 'downloader/request_count', 'downloader/response_count', 'downloader/response_status_count/200', 'item_scraped_count':
            r2.delete(keyname + "_" + "huxiu")
        print "pushing huxiu:start_url success"
    except Exception:
        print "pushing huxiu:start_url failed"
if __name__ == '__main__':
    init()
