# -*- coding: utf-8 -*-
import redis
import mi.settings as prime_settings
class MonitorInit(object):
    #框架在dupefilter的部分有bug，产生的redis队列在名字的末尾多一个0.暂时先手动加着
    def start(self):
        print "pushing start_url......"
        try:
            # 连接数据库
            r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db = prime_settings.FLASK_DB)
            # 清空monitor的四个队列
            r.delete(prime_settings.request_count)
            r.delete(prime_settings.response_count)
            r.delete(prime_settings.response_status200_count)
            r.delete(prime_settings.item_scraped_count)
            print "pushing start_url success"
        except Exception:
            print "pushing start_url failed"