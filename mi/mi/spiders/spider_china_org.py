# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
class Spider_china_org(RedisCrawlSpider):
    name = 'china_org'
    redis_key = 'china_org:start_urls'
    allowed_domains = ['china.org.cn']
    rules = [
        Rule(LinkExtractor(allow=('http://www.china.org.cn/\w+/'),deny=()),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath('''//h1[@id='title']/text()''').extract()[0]
            content = ''.join(response.xpath('''//div[@class='apDiv1']/div[@id='container_txt']/p/text()''').extract())
            item['articleTitle'] = title
            item['articleUrl'] = ''.join(response.url)
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
