# -*- coding: utf-8 -*-
import redis
def init():
    print "pushing finance_ifeng:start_url......"
    try:
        r = redis.Redis("192.168.139.239", 7001, 0)
        r.delete("finance_ifeng:start_urls")
        r.delete("finance_ifeng:dupefilter" + "0")
        r.delete("finance_ifeng:requests")
        r.lpush("finance_ifeng:start_urls", 'http://finance.ifeng.com')
        r2 = redis.Redis("192.168.139.239", 7001, 15)
        for keyname in 'downloader/request_count', 'downloader/response_count', 'downloader/response_status_count/200', 'item_scraped_count':
            r2.delete(keyname + "_" + "finance_ifeng")
        print "pushing finance_ifeng:start_url success"
    except Exception:
        print "pushing finance_ifeng:start_url failed"
if __name__ == '__main__':
    init()
