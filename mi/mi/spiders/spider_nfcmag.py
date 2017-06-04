# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
class Spider_nfcmag(RedisCrawlSpider):
    name = 'nfcmag'
    redis_key = 'nfcmag:start_urls'
    allowed_domains = ['nfcmag.com']
    rules = [
        Rule(LinkExtractor(allow=('http://www.nfcmag.com/article/\d+'),deny=()),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath('''//div[@class='article-content-box']/h3/text()''').extract()[0]
            content = ''.join(response.xpath('''//div[@class='content']/p/text()''').extract())
            item['articleTitle'] = title
            item['articleUrl'] = ''.join(response.url)
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
