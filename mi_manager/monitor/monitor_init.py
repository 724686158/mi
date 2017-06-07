# -*- coding: utf-8 -*-
import redis
import settings as prime_settings
class MonitorInit(object):
    def start(self):
        print "尝试清空主监控器记录"
        try:
            # 连接数据库
            r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db = prime_settings.MONITOR_DB)
            r.flushdb()
            # 清空monitor的四个队列
            for keyname in prime_settings.STATS_KEYS:
                r.delete(keyname)
            print "清空主监控器记录成功"
        except Exception:
            print "清空主监控器记录失败"
        finally:
            pass