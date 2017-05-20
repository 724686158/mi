# -*- coding: utf-8 -*-
import os
import monitor_settings

def arr2str(arr):
    return ', '.join(map(lambda x: "'" + x + "'", arr))

# 爬虫初始化文件模板
spider_init_template = \
"""# -*- coding: utf-8 -*-
import redis
def init():
    print "pushing %s:start_url......"
    try:
        r = redis.Redis("%s", %s, %s)
        r.delete("%s:start_urls")
        r.delete("%s:dupefilter" + "0")
        r.delete("%s:requests")
        r.lpush("%s:start_urls", %s)
        r2 = redis.Redis("%s", %s, %s)
        for keyname in %s:
            r2.delete(keyname + "_" + "%s")
        print "pushing %s:start_url success"
    except Exception:
        print "pushing %s:start_url failed"
if __name__ == '__main__':
    init()
"""

# 传入字典格式的字符串
def generate_spider_init(jsonfile):
    dic = eval(jsonfile)
    arr = (
        dic['name'],
        monitor_settings.REDIS_HOST,
        monitor_settings.REDIS_PORT,
        monitor_settings.FILTER_DB,
        dic['name'],
        dic['name'],
        dic['name'],
        dic['name'],
        arr2str(dic['start_urls']),
        monitor_settings.REDIS_HOST,
        monitor_settings.REDIS_PORT,
        monitor_settings.MONITOR_DB,
        arr2str(monitor_settings.STATS_KEYS),
        dic['name'],
        dic['name'],
        dic['name'])
    ok = spider_init_template % arr
    filename = os.getcwd() + '/monitor/spiderinit_files/spiderInit_' + dic['name'] + '.py'
    with open(filename, 'w') as f:
        f.write(ok.encode('utf8'))
