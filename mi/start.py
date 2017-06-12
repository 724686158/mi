#-*- coding: utf-8 -*-
import redis
import scrapy.cmdline as cmd
from tld import get_tld
import mi.settings as prime_settings
import mi.tools.gen_spiderFile_in_whiteList as gen_spiderFile_in_whiteList
import mi.tools.gen_spiderFile_need_fuzzymatching as gen_spiderFile_need_fuzzymatching

if __name__ == '__main__':

    r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db=prime_settings.MISSIONS_DB)
    r2 = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db=prime_settings.SPIDERS_DB)
    try:
        news_in_whitelist_urls = r.lrange('1', 0, -1)
        for mission in news_in_whitelist_urls:
            spidername = get_tld(mission, fail_silently=True)
            attr = r2.get(spidername)
            bo = gen_spiderFile_in_whiteList.generate_spider(spidername, attr)
            if bo == True:
                print '加载新闻爬虫(白名单)文件成功'
            else:
                print '加载新闻爬虫(白名单)文件失败'
    except:
        print '加载新闻爬虫(白名单)文件失败'
    news_need_fuzzymatching_urls = r.lrange('0', 0, -1)
    for mission in news_need_fuzzymatching_urls:
        spidername = get_tld(mission, fail_silently=True)
        bo = gen_spiderFile_need_fuzzymatching.generate_spider(spidername)
        if bo == True:
            print '加载新闻爬虫(模糊匹配)文件成功'
        else:
            print '加载新闻爬虫(模糊匹配)文件失败'
    try:
        pass
    except:
        print '加载新闻爬虫(模糊匹配)文件失败'

    cmd.execute('scrapy crawlall'.split())