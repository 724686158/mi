# -*- coding: utf-8 -*-
import redis
import random
import json
from scrapy.downloadermiddlewares.retry import RetryMiddleware

class CookieMiddleware(RetryMiddleware):
    # 用于初始化,与实际服务无关
    r = redis.Redis(host="127.0.0.1", port="6379", db=0)

    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)
        REDIS_HOST = settings.get('REDIS_HOST')
        REDIS_PORT = settings.get('REDIS_PORT')
        REDIS_DB = settings.get('COOKIES_DB')
        self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)#decode_responses设置取出的编码为str
        self.init_cookie(crawler.spider.name)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def process_request(self, request, spider):
        print 'cookie中间件工作中'
        redis_keys = self.r.keys()
        users = self.r.lrange(spider.name, 0, -1)
        if users is not None:
            print '此爬虫需要使用cookie'
            while len(redis_keys) > 0:
                elem = random.choice(redis_keys)
                if spider.name + ':Cookies' in elem:
                    cookie = json.loads(self.r.get(elem))
                    request.cookies = cookie
                    break
        else:
            print '此爬虫不需要使用cookie'

    def init_cookie(self, spidername):
        redis_keys = self.r.keys()
        users = self.r.lrange(spidername, 0, -1)
        if users is not None:
            for user in users:
                if self.r.get("%s:Cookies:%s" % (spidername, user)) is None:
                    cookie = self.get_cookie(user)
                    self.r.set("%s:Cookies:%s" % (spidername, user), cookie)


    def get_cookie(self, spidername, account):
        if spidername == 'taobao':
            taobao_cookie = {
                '_tb_token_': 'wSPfJ0NvWxDT',
                'ck1': '',
                'login': 'true',
                'cna': 'K1GCEYAqd2QCAXWIXAhhKY/B',
                'ubn': 'p',
                'l': 'AkxMGcuoSJDWzQ46-YjRYggcnKF-kPAv',
                'isg': 'AtHRDN1vbOUdX4EIbreFWVbb4NvKhEWw1etGsbNm2Bi3WvGs-45VgH_6iphH',
                'uss': 'VFO9RjW7odubU2obnLsFHSTKEDfX0836GnlA0i4Upb4kKfZl8suhO7NnOg%3D%3D',
                'hng': '',
                'cookie17': 'UUtIEnrP5E0Tkw%3D%3D',
                '_l_g_': 'Ug%3D%3D',
                '_nk_': account,
                'skt': '42012dc6097690ef',
                't': '83ced636d91d9a7a0100d841394e8314',
                'unb': '2337902764',
                'cookie1': 'UITvcaq6VhvgPGaFwm9IOSo0iYrD7smV4b8taUoPzRc%3D',
                'cookie2': '1c51ff19423199f5bfe7aebfe5164da3',
                'tracknick': account,
                'lgc': account
            }
            return json.dumps(taobao_cookie)
        else:
            return None


    def update_cookie(self):
        self.r = redis.Redis()

    def remove_cookie(self, spidername, account):
        self.r.delete("%s:Cookies:%s" % (spidername, account))
