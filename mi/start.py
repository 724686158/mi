#-*- coding: utf-8 -*-
import scrapy.cmdline as cmd
import mi.settings as prime_settings
import redis
from tld import get_tld
from mi.commands.gen_spiderFile import generate_spider
if __name__ == '__main__':

    r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db=prime_settings.MISSIONS_DB)
    missions = r.lrange('1', 0, -1)
    r2 = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db=prime_settings.SPIDERS_DB)
    for mission in missions:
        spidername = get_tld(mission, fail_silently=True)
        attr = r2.get(spidername)
        bo = generate_spider(attr)
    cmd.execute('scrapy crawlall'.split())

