# -*- coding: utf-8 -*-
import redis
import mi.settings as prime_settings
from mysqlHelper import MysqlHelper
def init():
    print "try insert eCommerceId......"
    try:
        db = MysqlHelper()
        sql = "insert into ECommerce(eCommerceId, eCommerceName, eCommerceUrl) values( 2, 'taobao', 'https://www.taobao.com');".encode(encoding='utf-8')
        db.insert(sql)
        print "insert eCommerceId success"
    except Exception:
        print "insert eCommerceId failed"

    print "pushing taobao:start_url......"
    try:
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT)
        r.delete("taobao:start_urls")
        r.delete("taobao:dupefilter" + "0")
        r.delete("taobao:requests")
        r.lpush("taobao:start_urls", 'https://item.taobao.com/item.htm?id=543531240663')
        print "pushing taobao:start_url success"
    except Exception:
        print "pushing taobao:start_url failed"
if __name__ == '__main__':
    init()
