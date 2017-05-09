# -*- coding: utf-8 -*-
import json
def arr2str(arr):
    return ', '.join(map(lambda x: "'" + x + "'", arr))

#爬虫初始化模板
spider_init_template = \
"""# -*- coding: utf-8 -*-
import redis
import mi.settings as prime_settings
def init():
    print "pushing %s:start_url......"
    try:
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT)
        r.delete("%s:start_urls")
        r.delete("%s:dupefilter" + "0")
        r.delete("%s:requests")
        r.lpush("%s:start_urls", %s)
        print "pushing %s:start_url success"
    except Exception:
        print "pushing %s:start_url failed"
if __name__ == '__main__':
    init()
"""
def generate_spider_init(jsonfile):
    print jsonfile
    js = dict(json.loads(jsonfile))
    arr = (
        js['name'],
        js['name'],
        js['name'],
        js['name'],
        js['name'],
        arr2str(js['start_urls']),
        js['name'],
        js['name'])
    ok = spider_init_template % arr
    filename = "../monitor/spiderInit/" + "spiderInit_" + js['name'] + ".py"
    with open(filename, 'w') as f:
        f.write(ok.encode('utf8'))
