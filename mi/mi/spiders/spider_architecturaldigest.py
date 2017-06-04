# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
class Spider_architecturaldigest(RedisCrawlSpider):
    name = 'architecturaldigest'
    redis_key = 'architecturaldigest:start_urls'
    allowed_domains = ['architecturaldigest.in']
    rules = [
        Rule(LinkExtractor(allow=('https://www.architecturaldigest.in/content/\w+'),deny=()),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath('''//h1/text()''').extract()[0]
            content = ''.join(response.xpath('''//article/p/text()''').extract())
            item['articleTitle'] = title
            item['articleUrl'] = ''.join(response.url)
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
