#-*- coding: utf-8 -*-
import os
import redis
import scrapy.cmdline as cmd
import mi.settings as prime_settings
import mi.tools.gen_spiderFile_in_whiteList as gen_spiderFile_in_whiteList
import mi.tools.gen_spiderFile_need_fuzzymatching as gen_spiderFile_need_fuzzymatching
import gen_settings
def init_spider_file(task):
    dic = eval(task)
    spidername = dic['spider_name']
    oscwd = os.getcwd()
    filename = oscwd + '/mi/spiders_of_eCommerce' + '/spider_' + str(spidername).split('.')[0] + '.py'
    if os.path.isfile(filename):
        pass
    else:
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db=prime_settings.SPIDERS_DB)
        if spidername in r.keys():
            gen_spiderFile_in_whiteList.generate_spider(spidername, r.get(spidername))
        else:
            gen_spiderFile_need_fuzzymatching.generate_spider(spidername)

def init_settings(task):
    gen_settings.generate_setting_of_mi(task)

def start_work(task):
    dic = eval(task)
    spider_name = dic['spider_name']
    start_url = dic['start_url']
    r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db=prime_settings.FILTER_DB)
    r.lpush(spider_name +':start_urls', start_url)
    print '将对', spider_name, '进行爬取'
    cmd.execute(str('scrapy crawl ' + spider_name).split())

if __name__ == '__main__':
    try:
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db=prime_settings.TASK_DB)
        task = r.rpop('ready')
        if task:
            print '开始执行任务'
            init_settings(task)
            init_spider_file(task)
            start_work(task)
            r.lpush('used', task)
        else:
            print '没有需要执行的任务'
    except:
        print '无法连接至核心数据库'
