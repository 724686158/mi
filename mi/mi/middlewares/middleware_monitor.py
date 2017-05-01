# -*- coding: utf-8 -*-
import redis
import time



Time = lambda: time.strftime('%Y-%m-%d %H:%M:%S')

class StatcollectorMiddleware(object):
    # 用于初始化,与实际服务无关
    r = redis.Redis(host="127.0.0.1", port="6379", db=0)
    timer = lambda: time.strftime('%Y-%m-%d %H:%M:%S')
    def __init__(self, settings):
        REDIS_HOST = settings.get('REDIS_HOST')
        REDIS_PORT = settings.get('REDIS_PORT')
        REDIS_DB = settings.get('FLASK_DB')
        STATS_KEYS = settings.get('STATS_KEYS')
        self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        self.stats_keys = STATS_KEYS

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        self.formatStats(spider.crawler.stats.get_stats())

    def formatStats(self, stats):
        time = Time()
        arr = []
        for key in self.stats_keys:
            key_value = stats.get(key, None)
            if not key_value: continue
            value = {"value": [time, key_value]}
            arr.append(value)
        if len(arr) == len(self.stats_keys):
            con = 0
            for key in self.stats_keys:
                self.r.rpush(key, arr[con])
                con = con + 1