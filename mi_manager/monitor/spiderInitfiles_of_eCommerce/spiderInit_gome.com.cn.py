# -*- coding: utf-8 -*-
import redis
import monitor.settings as prime_settings
from monitor.mysqlHelper import MysqlHelper

def init():
    print "try insert eCommerceId......"
    try:
        db = MysqlHelper()
        sql = "insert into ECommerce(eCommerceName, eCommerceUrl) values('gome.com.cn', 'http://www.gome.com.cn');".encode(encoding='utf-8')
        db.insert(sql)
        print "insert eCommerceId success"
    except Exception:
        print "insert eCommerceId failed"

    print "pushing guomei:start_url......"
    try:
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db=prime_settings.FILTER_DB)
        r.delete("guomei:start_urls")
        r.delete("guomei:dupefilter" + "0")
        r.delete("guomei:requests")
        r.lpush("guomei:start_urls", 'http://www.gome.com.cn')
        print "pushing guomei:start_url success"
    except Exception:
        print "pushing guomei:start_url failed"
if __name__ == '__main__':
    init()
