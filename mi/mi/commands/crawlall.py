# -*- coding: utf-8 -*-
from scrapy.commands import ScrapyCommand
from scrapy.utils.conf import arglist_to_dict
import os
from mysql_init import MysqlInit
from monitor_init import MonitorInit
import subprocess

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
        monitor_init = MonitorInit()
        monitor_init.start()
        #初始化mysql数据库
        mysql_init = MysqlInit()
        mysql_init.start()

        spider_loader = self.crawler_process.spider_loader
        for spidername in args or spider_loader.list():
            print "*********cralall spidername************" + spidername
            # 整理爬虫所使用的redis队列
            os.system("python mi/commands/SpiderInit_" + spidername + ".py")
            self.crawler_process.crawl(spidername, **opts.spargs)
            self.crawler_process.start()
