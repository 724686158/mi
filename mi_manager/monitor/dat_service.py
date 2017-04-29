import json
import redis

HOST = '192.168.139.239'
PORT = 7001
DB_ID = 13


def save_data(spider_name, json_str):
    r = redis.Redis(HOST, PORT, DB_ID)
    js = dict(json.loads(json_str))
    r.set(spider_name, js)


def query_data(spider_name):
    r = redis.Redis(HOST, PORT, DB_ID)
    print r.get(spider_name)
