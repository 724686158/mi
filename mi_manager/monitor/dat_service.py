import json
import redis
from tld import get_tld
import chardet

HOST = '192.168.139.239'
PORT = 7001
DB_ID = 13


def get_redis():
    return redis.Redis(HOST, PORT, DB_ID)


def save_data(spider_name, json_str):
    r = get_redis()
    js = dict(json.loads(json_str))
    r.set(spider_name, js)


def query_data(spider_name):
    r = get_redis()
    print r.get(spider_name)


def split_target_urls(urls):
    r = get_redis()
    st = set()
    for i in r.keys():
        st.add(unicode(i, 'utf8'))
    A, B = [], []
    map(lambda url: A.append(url) if get_tld(url, fail_silently=True) in st else B.append(url), urls)
    return A, B
