# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
class Spider_jianglishi(RedisCrawlSpider):
    name = 'jianglishi'
    redis_key = 'jianglishi:start_urls'
    allowed_domains = ['jianglishi.cn']
    rules = [
        Rule(LinkExtractor(allow=('http://www.jianglishi.cn/\w+/\d+'),deny=()),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath('''//div[@class='wrap']/div/h1/text()''').extract()[0]
            content = ''.join(response.xpath('''//div[@class='wrap']/div/div[@class='content_text']/p/text()''').extract())
            item['articleTitle'] = title
            item['articleUrl'] = ''.join(response.url)
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
