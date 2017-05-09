# -*- coding: utf-8 -*-
import mi.settings as settings
import redis
import requests

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.MONITOR_DB)
class SpiderRunStatspipeline(object):
    def open_spider(self, spider):

        r.set('spider_is_run', 1)
        try:
            requests.get('http://' + settings.MONITOR_HOST + ':' + str(settings.MONITOR_PORT) + '/signal?sign=running')
        except requests.exceptions.ConnectionError:
            r.status_code = "Connection refused"


    def close_spider(self, spider):
        r.set('spider_is_run', 0)
        try:
            requests.get('http://' + settings.MONITOR_HOST + ':' + str(settings.MONITOR_PORT) + '/signal?sign=closed')
        except requests.exceptions.ConnectionError:
            r.status_code = "Connection refused"
