# -*- coding: utf-8 -*-
import os
import json
import redis
import settings
from monitor_init import MonitorInit
from mysql_init import MysqlInit
from tld import get_tld
from gen_spiderInitfile_of_news import generate_spider_init

def get_redis(db_id):
    return redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, db_id)

def save_proxys(proxys):
    r = get_redis(settings.PROXY_DB)
    for proxy in proxys:
        r.lpush('valid_proxy',proxy)

def save_data(spider_name, json_str):
    r = get_redis(settings.SPIDERS_DB)
    js = dict(json.loads(json_str))
    r.set(spider_name, js)


def query_data(spider_name):
    r = get_redis(settings.SPIDERS_DB)


def get_whitelist():
    r = get_redis(settings.SPIDERS_DB)
    st = set()
    for i in r.keys():
        st.add(unicode(i, 'utf8'))
    return st

def split_target_urls(urls):
    keys = get_whitelist()
    r = get_redis(settings.MISSIONS_DB)
    # 获取新任务后清空数据库
    r.flushdb()
    oscwd = os.getcwd()
    for url in urls:
        spidername = get_tld(url, fail_silently=True)
        filename = oscwd + settings.TEMP_PATH + '/spiderInitfiles_of_eCommerce' + '/spiderInit_' + spidername + '.py'
        if os.path.isfile(filename):
            r.rpush(2, url)
        elif spidername in keys:
            r.rpush(1, url)
            generate_spider_init(spidername, {url})
        else:
            r.rpush(0, url)
            generate_spider_init(spidername, {url})


def get_spider_count_from_db():
    r = get_redis(settings.MONITOR_DB)
    keys = r.keys()
    arr = []
    for i in keys:
        if 'item_scraped_count_' in i:
            arr.append(i[i.rfind('_') + 1:])
    return arr

def init_monitor():
    # 初始化监控器数据
    monitor_init = MonitorInit()
    monitor_init.start()

def init_mysql():
    # 初始化mysql数据库
    mysql_init = MysqlInit()
    mysql_init.start()

def exec_init_of_missions():
    oscwd = os.getcwd()
    r = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, db=settings.MISSIONS_DB)
    news_spiders_need_fuzzymatching = r.lrange('0', 0, -1)
    news_spiders_in_whitelist = r.lrange('1', 0, -1)
    mission_urls = news_spiders_in_whitelist + news_spiders_need_fuzzymatching
    for mission_url in mission_urls:
        mission = get_tld(mission_url, fail_silently=True)
        filename =  oscwd + settings.TEMP_PATH + '/spiderInitfiles_of_news' + '/spiderInit_' + mission + '.py'
        if os.path.isfile(filename):
            print filename
            os.system('python2 ' + filename)
        else:
            print 'news_spider Init_' + mission + '.py' + ' not exist'

    ec_spiders = r.lrange('2', 0, -1)
    for mission_url in ec_spiders:
        mission = get_tld(mission_url, fail_silently=True)
        filename =  oscwd + settings.TEMP_PATH + '/spiderInitfiles_of_eCommerce' + '/spiderInit_' + mission + '.py'
        if os.path.isfile(filename):
            print filename
            os.system('python2 ' + filename)
        else:
            print 'eCommerce_spider Init_' + mission + '.py' + ' not exist'
