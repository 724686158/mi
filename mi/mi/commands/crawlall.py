# -*- coding: utf-8 -*-
import redis
import scrapy.cmdline as cmd
import mi.settings as prime_settings
from scrapy.commands import ScrapyCommand
from scrapy.utils.conf import arglist_to_dict
from tld import get_tld
from gen_spiderFile import generate_spider



class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
                          help="set spider argument (may be repeated)")
        parser.add_option("-o", "--output", metavar="FILE",
                          help="dump scraped items into FILE (use - for stdout)")
        parser.add_option("-t", "--output-format", metavar="FORMAT",
                          help="format to use for dumping items with -o")

    def process_options(self, args, opts):
        ScrapyCommand.process_options(self, args, opts)
        try:
            opts.spargs = arglist_to_dict(opts.spargs)
        except ValueError:
            from scrapy.exceptions import UsageError
            raise UsageError("Invalid -a value, use -a NAME=VALUE", print_help=False)

    def run(self, args, opts):
        # 初始化爬虫文件
        '''
        bo = self.init_spiderfiles()
        if bo:
            print '加载爬虫文件成功'
        else:
            print '加载爬虫文件失败'
        :param args:
        :param opts:
        :return:
        '''
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db=prime_settings.MISSIONS_DB)
        missions = r.lrange('1', 0, -1)
        r2 = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db=prime_settings.SPIDERS_DB)
        for mission in missions:
            spidername = get_tld(mission, fail_silently=True)
            attr = r2.get(spidername)
            dic = eval(attr)
            print dic['name']
            self.crawler_process.crawl(dic['name'], **opts.spargs)
            self.crawler_process.start()



    def init_spiderfiles(self):
        try:
            r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db=prime_settings.MISSIONS_DB)
            missions = r.lrange('1', 0, -1)
            r2 = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db = prime_settings.SPIDERS_DB)
            for mission in missions:
                spidername = get_tld(mission, fail_silently=True)
                attr = r2.get(spidername)
                bo = generate_spider(attr)
                if bo != True:
                    return False
            return True
        except:
            return False

