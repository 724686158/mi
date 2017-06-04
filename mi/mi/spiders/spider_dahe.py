# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
class Spider_dahe(RedisCrawlSpider):
    name = 'dahe'
    redis_key = 'dahe:start_urls'
    allowed_domains = ['dahe.cn']
    rules = [
        Rule(LinkExtractor(allow=('news.dahe.cn/\d{4}/\d{2}-\d{2}/\d+'),deny=()),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath('''//h1[@id='4g_title']/text()''').extract()[0]
            content = ''.join(response.xpath('''//div[@id='mainCon']/p/text()''').extract())
            item['articleTitle'] = title
            item['articleUrl'] = ''.join(response.url)
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
