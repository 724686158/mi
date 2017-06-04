# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
class Spider_finance_ifeng(RedisCrawlSpider):
    name = 'finance_ifeng'
    redis_key = 'finance_ifeng:start_urls'
    allowed_domains = ['finance.ifeng.com']
    rules = [
        Rule(LinkExtractor(allow=('finance.ifeng.com/a/\d{8}'),deny=()),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath('''//div[@id='artical']/h1/text()''').extract()[0]
            content = ''.join(response.xpath('''//div[@id='main_content']/p/text()''').extract())
            item['articleTitle'] = title
            item['articleUrl'] = ''.join(response.url)
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
