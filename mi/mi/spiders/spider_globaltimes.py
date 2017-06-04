# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
class Spider_globaltimes(RedisCrawlSpider):
    name = 'globaltimes'
    redis_key = 'globaltimes:start_urls'
    allowed_domains = ['globaltimes.cn']
    rules = [
        Rule(LinkExtractor(allow=('http://www.globaltimes.cn/content/\w+'),deny=()),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath('''//div[@id='contents']/div/div/h3/text()''').extract()[0]
            content = ''.join(response.xpath('''//div[@id='contents']/div/div/div[@class='span12 row-content']/text() | //div[@id='contents']/div/div[@class='row-fluid'][1]/div[@class='span12 row-content']/p/text()''').extract())
            item['articleTitle'] = title
            item['articleUrl'] = ''.join(response.url)
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
