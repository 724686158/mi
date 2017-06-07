# -*- coding: utf-8 -*-
import redis
import monitor.settings as prime_settings
from monitor.mysqlHelper import MysqlHelper


def init():
    print "try insert eCommerceId......"
    try:
        db = MysqlHelper()
        sql = "insert into ECommerce(eCommerceName, eCommerceUrl) values('jd.com', 'https://item.jd.com');".encode(encoding='utf-8')
        db.insert(sql)
        print "insert eCommerceId success"
    except Exception:
        print "insert eCommerceId failed"

    print "pushing jd:start_url......"
    try:
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db=prime_settings.FILTER_DB)
        r.delete("jd:start_urls")
        r.delete("jd:dupefilter" + "0")
        r.delete("jd:requests")
        r.lpush("jd:start_urls", 'https://item.jd.com/3312381.html')
        print "pushing jd:start_url success"
    except Exception:
        print "pushing jd:start_url failed"
if __name__ == '__main__':
    init()
