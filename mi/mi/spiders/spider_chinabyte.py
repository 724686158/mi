# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
class Spider_chinabyte(RedisCrawlSpider):
    name = 'chinabyte'
    redis_key = 'chinabyte:start_urls'
    allowed_domains = ['chinabyte.com']
    rules = [
        Rule(LinkExtractor(allow=('http://it.chinabyte.com/\w+/'),deny=()),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath('''//div[@class='hot_art']/h1/text()''').extract()[0]
            content = ''.join(response.xpath('''//div[@class='art_txt']/div[2]/p/text()''').extract())
            item['articleTitle'] = title
            item['articleUrl'] = ''.join(response.url)
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
