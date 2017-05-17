# -*- coding: utf-8 -*-
import json
import redis
import monitor_settings
from tld import get_tld
from gen_spiderInitfile import generate_spider_init
def get_redis(db_id):
    return redis.Redis(monitor_settings.REDIS_HOST, monitor_settings.REDIS_PORT, db_id)

def save_proxys(proxys):
    r = get_redis(monitor_settings.PROXY_DB)
    for proxy in proxys:
        r.lpush('valid_proxy',proxy)

def save_data(spider_name, json_str):
    r = get_redis(monitor_settings.SPIDERS_DB)
    js = dict(json.loads(json_str))
    r.set(spider_name, js)


def query_data(spider_name):
    r = get_redis(monitor_settings.SPIDERS_DB)


def get_site_key():
    r = get_redis(monitor_settings.SPIDERS_DB)
    st = set()
    for i in r.keys():
        st.add(unicode(i, 'utf8'))
    return st

def split_target_urls(urls):
    keys = get_site_key()
    r = get_redis(monitor_settings.MISSIONS_DB)
    # 获取新任务后清空数据库
    r.flushdb()
    for url in urls:
        spidername = get_tld(url, fail_silently=True)
        if spidername in keys:
            r.rpush(1, url)
            r2 = get_redis(monitor_settings.SPIDERS_DB)
            attr = r2.get(spidername)
            generate_spider_init(attr)
        else:
            r.rpush(0, url)

def get_spider_count_from_db():
    r = get_redis(monitor_settings.MONITOR_DB)
    keys = r.keys()
    arr = []
    for i in keys:
        if 'item_scraped_count_' in i:
            arr.append(i[i.rfind('_') + 1:])
    return arr
