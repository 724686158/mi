# -*- coding: utf-8 -*-
import os
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
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, prime_settings.FILTER_DB)
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

# 传入字典格式的字符串
def generate_spider_init(jsonfile):
    dic = eval(jsonfile)
    print dic['name']
    arr = (
        dic['name'],
        dic['name'],
        dic['name'],
        dic['name'],
        dic['name'],
        arr2str(dic['start_urls']),
        dic['name'],
        dic['name'])
    ok = spider_init_template % arr
    filename = os.getcwd() + '/mi/commands/spiderInit_' + dic['name'] + '.py'
    with open(filename, 'w') as f:
        f.write(ok.encode('utf8'))
