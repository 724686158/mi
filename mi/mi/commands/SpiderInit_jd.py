# -*- coding: utf-8 -*-
import redis
import mi.settings as prime_settings
from mysqlHelper import MysqlHelper
def init():
    print "try insert eCommerceId......"
    try:
        db = MysqlHelper()
        sql = "insert into ECommerce(eCommerceId, eCommerceName, eCommerceUrl) values( 1, 'jd', 'https://item.jd.com');".encode(encoding='utf-8')
        db.insert(sql)
        print "insert eCommerceId success"
    except Exception:
        print "insert eCommerceId failed"

    print "pushing caijing_start_url......"
    try:
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT)
        r.delete("jd:start_urls")
        r.delete("jd:dupefilter" + "0")
        r.delete("jd:requests")
        r.lpush("jd:start_urls", 'https://item.jd.com/3312381.html')
        print "pushing jd_start_url success"
    except Exception:
        print "pushing jd_start_url failed"
if __name__ == '__main__':
    init()
