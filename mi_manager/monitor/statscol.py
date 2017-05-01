# -*- coding: utf-8 -*-
import redis
from monitor_settings import *
import time
import requests

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
Time = lambda: time.strftime('%Y-%m-%d %H:%M:%S')


class StatcollectorMiddleware(object):
    def __init__(self):
        self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        self.stats_keys = STATS_KEYS

    def process_request(self, request, spider):
        self.formatStats(spider.crawler.stats.get_stats())

    def formatStats(self, stats):
        for key in self.stats_keys:
            key_value = stats.get(key, None)
            if not key_value: continue
            value = {"value": [Time(), key_value]}
            self.insert2redis(key, value)

    def insert2redis(self, key, value):
        self.r.rpush(key, value)


class SpiderRunStatspipeline(object):
    def open_spider(self, spider):

        r.set('spider_is_run', 1)
        try:
            page1 = requests.get('http://' + REDIS_HOST + ':' + str(REDIS_PORT) + '/signal?sign=running')
        except requests.exceptions.ConnectionError:
            r.status_code = "Connection refused"


    def close_spider(self, spider):
        r.set('spider_is_run', 0)
        try:
            page1 = requests.get('http://' + REDIS_HOST + ':' + str(REDIS_PORT) + '/signal?sign=closed')
        except requests.exceptions.ConnectionError:
            r.status_code = "Connection refused"
