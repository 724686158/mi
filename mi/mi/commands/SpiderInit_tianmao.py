# -*- coding: utf-8 -*-
import redis
import mi.settings as prime_settings
from mysqlHelper import MysqlHelper
def init():
    print "try insert eCommerceId......"
    try:
        db = MysqlHelper()
        sql = "insert into ECommerce(eCommerceId, eCommerceName, eCommerceUrl) values( 3, 'tianmao', 'https://www.tmall.com');".encode(encoding='utf-8')
        db.insert(sql)
        print "insert eCommerceId success"
    except Exception:
        print "insert eCommerceId failed"

    print "pushing tianmao:start_url......"
    try:
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db = prime_settings.FILTER_DB)
        r.delete("tianmao:start_urls")
        r.delete("tianmao:dupefilter" + "0")
        r.delete("tianmao:requests")
        r.lpush("tianmao:start_urls", 'https://detail.tmall.com/item.htm?id=536825175726')
        print "pushing tianmao:start_url success"
    except Exception:
        print "pushing tianmao:start_url failed"

    try:
        print "尝试加入cookie用户帐号信息..."
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db = prime_settings.COOKIES_DB)
        r.lpush("tianmao", 'omtbreak')
        print "尝试加入cookie用户帐号信息成功"
    except Exception:
        print "尝试加入cookie用户帐号信息失败"
if __name__ == '__main__':
    init()
