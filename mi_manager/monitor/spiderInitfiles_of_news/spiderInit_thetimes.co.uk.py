# -*- coding: utf-8 -*-
import redis
def init():
    print "pushing thetimes.co.uk:start_url......"
    try:
        r = redis.Redis("192.168.139.239", 7001, 0)
        r.delete("thetimes.co.uk:start_urls")
        r.delete("thetimes.co.uk:dupefilter" + "0")
        r.delete("thetimes.co.uk:requests")
        r.lpush("thetimes.co.uk:start_urls", 'https://www.thetimes.co.uk/edition/sport/members-to-decide-on-150m-lords-facelift-8ss0ftrqd')
        r2 = redis.Redis("192.168.139.239", 7001, 15)
        for keyname in 'downloader/request_count', 'downloader/response_count', 'downloader/response_status_count/200', 'item_scraped_count':
            r2.delete(keyname + "_" + "thetimes.co.uk")
        print "pushing thetimes.co.uk:start_url success"
    except Exception:
        print "pushing thetimes.co.uk:start_url failed"
if __name__ == '__main__':
    init()
