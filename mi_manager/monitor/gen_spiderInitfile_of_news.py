# -*- coding: utf-8 -*-
import os
import settings

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
def generate_spider_init(name, start_urls):
    arr = (
        name,
        settings.REDIS_HOST,
        settings.REDIS_PORT,
        settings.FILTER_DB,
        name,
        name,
        name,
        name,
        arr2str(start_urls),
        settings.REDIS_HOST,
        settings.REDIS_PORT,
        settings.MONITOR_DB,
        arr2str(settings.STATS_KEYS),
        name,
        name,
        name)
    ok = spider_init_template % arr
    filename = os.getcwd() + settings.TEMP_PATH + '/spiderInitfiles_of_news/spiderInit_' + name + '.py'
    with open(filename, 'w') as f:
        f.write(ok.encode('utf8'))
