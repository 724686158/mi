# -*- coding: utf-8 -*-
import json
import redis
from tld import get_tld
import monitor_settings

HOST = '192.168.139.239'
PORT = 7001
DB_ID = 13


def get_redis(db_id=DB_ID):
    return redis.Redis(HOST, PORT, db_id)


def save_data(spider_name, json_str):
    r = get_redis()
    js = dict(json.loads(json_str))
    r.set(spider_name, js)


def query_data(spider_name):
    r = get_redis()
    print r.get(spider_name)


def get_site_key():
    r = get_redis()
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
        if get_tld(url, fail_silently=True) in keys:
            r.rpush(1, url)
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
