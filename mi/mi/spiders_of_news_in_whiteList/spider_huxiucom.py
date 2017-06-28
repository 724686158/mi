# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
class Spider_huxiu(RedisCrawlSpider):
    name = 'huxiu.com'
    redis_key = 'huxiu.com:start_urls'
    allowed_domains = ['huxiu.com']
    rules = [
        Rule(LinkExtractor(allow=('https://www.huxiu.com/article/'),deny=()),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath('''//h1/text()''').extract()[0]
            content = ''.join(response.xpath('''//div[@class='article-content-wrap']//p/text()''').extract())
            item['articleTitle'] = title
            item['articleUrl'] = ''.join(response.url)
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
