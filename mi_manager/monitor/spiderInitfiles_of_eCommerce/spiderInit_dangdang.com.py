# -*- coding: utf-8 -*-
import redis
import monitor.settings as prime_settings
from monitor.mysqlHelper import MysqlHelper

def init():
    print "try insert eCommerceId......"
    try:
        db = MysqlHelper()
        sql = "insert into ECommerce(eCommerceName, eCommerceUrl) values('dangdang.com', 'http://www.dangdang.com');".encode(encoding='utf-8')
        db.insert(sql)
        print "insert eCommerceId success"
    except Exception:
        print "insert eCommerceId failed"

    print "pushing dangdang:start_url......"
    try:
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db=prime_settings.FILTER_DB)
        r.delete("dangdang:start_urls")
        r.delete("dangdang:dupefilter" + "0")
        r.delete("dangdang:requests")
        r.lpush("dangdang:start_urls", 'http://www.dangdang.com')
        print "pushing dangdang:start_url success"
    except Exception:
        print "pushing dangdang:start_url failed"
if __name__ == '__main__':
    init()
