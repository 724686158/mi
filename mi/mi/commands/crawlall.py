# -*- coding: utf-8 -*-
import redis
from scrapy.commands import ScrapyCommand
from scrapy.utils.conf import arglist_to_dict
from tld import get_tld

import mi.settings as prime_settings
from mi.tools.gen_spiderFile_in_whiteList import generate_spider


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
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db=prime_settings.TASK_DB)
        news_spiders_need_fuzzymatching = r.lrange('0', 0, -1)
        news_spiders_in_whitelist = r.lrange('1', 0, -1)
        ec_spiders = r.lrange('2', 0, -1)
        all_urls = news_spiders_need_fuzzymatching + news_spiders_in_whitelist + ec_spiders
        for url in all_urls:
            spidername = get_tld(url, fail_silently=True)
            self.crawler_process.crawl(spidername, **opts.spargs)
            self.crawler_process.start()

    def init_spiderfiles(self):
        try:
            r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db=prime_settings.TASK_DB)
            missions = r.lrange('1', 0, -1)
            r2 = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db = prime_settings.SPIDERS_DB)
            for mission in missions:
                spidername = get_tld(mission, fail_silently=True)
                attr = r2.get(spidername)
                bo = generate_spider(spidername, attr)
                if bo != True:
                    return False
            return True
        except:
            return False

