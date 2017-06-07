#-*- coding: utf-8 -*-
import scrapy.cmdline as cmd
import mi.settings as prime_settings
import redis
from tld import get_tld
from mi.commands.gen_spiderFile_with_whiteList import generate_spider

'''
import threading
import thread
def worker(mission):
    cmd.execute(str('scrapy crawl ' + mission).split())
'''
if __name__ == '__main__':

    r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db=prime_settings.MISSIONS_DB)
    try:
        news_in_whitelist_urls = r.lrange('1', 0, -1)
        news_need_fuzzymatching_urls = r.lrange('0', 0, -1)
        r2 = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db=prime_settings.SPIDERS_DB)
        for mission in news_in_whitelist_urls:
            spidername = get_tld(mission, fail_silently=True)
            attr = r2.get(spidername)
            bo = generate_spider(spidername, attr)
            print '加载爬虫文件成功'
    except:
        print '加载爬虫文件失败'

    '''
    eCommerce_urls = r.lrange('2', 0, -1)
    for url in eCommerce_urls:
        mission = get_tld(url, fail_silently=True)
        t = thread.start_new_thread(worker, (mission))
        t.start()    
    '''
    cmd.execute('scrapy crawlall'.split())