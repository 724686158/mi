# -*- coding: utf-8 -*-
import redis
def init():
    print "pushing game58:start_url......"
    try:
        r = redis.Redis("192.168.139.239", 7001, 0)
        r.delete("game58:start_urls")
        r.delete("game58:dupefilter" + "0")
        r.delete("game58:requests")
        r.lpush("game58:start_urls", 'http://www.58game.com')
        r2 = redis.Redis("192.168.139.239", 7001, 15)
        for keyname in 'downloader/request_count', 'downloader/response_count', 'downloader/response_status_count/200', 'item_scraped_count':
            r2.delete(keyname + "_" + "game58")
        print "pushing game58:start_url success"
    except Exception:
        print "pushing game58:start_url failed"
if __name__ == '__main__':
    init()
