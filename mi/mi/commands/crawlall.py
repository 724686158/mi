# -*- coding: utf-8 -*-
from scrapy.commands import ScrapyCommand
from scrapy.utils.conf import arglist_to_dict
import os
from mysql_init import MysqlInit
from monitor_init import MonitorInit
import mi.settings as prime_settings
import subprocess
import redis
from gen_spiderFile import generate_spider
from gen_spiderInitFile import generate_spider_init
from tld import get_tld


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
        # 初始化监控器数据
        self.init_monitor()
        # 初始化mysql数据库
        self.init_mysql()
        # 初始化爬虫文件
        self.init_spiderfiles()

        spider_loader = self.crawler_process.spider_loader
        for spidername in args or spider_loader.list():
            print "*********cralall spidername************" + spidername
            self.crawler_process.crawl(spidername, **opts.spargs)
            self.crawler_process.start()

    def init_monitor(self):
        # 初始化监控器数据
        monitor_init = MonitorInit()
        monitor_init.start()

    def init_mysql(self):
        # 初始化mysql数据库
        mysql_init = MysqlInit()
        mysql_init.start()

    def init_spiderfiles(self):
        #清空旧有的爬虫文件爱你
        for filename in os.listdir(os.getcwd() + '/mi/spiders'):
            if 'spider_' in filename:
                os.remove(os.getcwd() + '/mi/spiders/' + filename)
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db = prime_settings.MISSIONS_DB)
        missions = r.lrange('1', 0, -1)
        r2 = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db = prime_settings.SPIDERS_DB)
        for mission in missions:
            spidername = get_tld(mission, fail_silently=True)
            attr = r2.get(spidername)
            generate_spider(attr)


