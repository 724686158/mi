# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
class Spider_thepaper(RedisCrawlSpider):
    name = 'thepaper.cn'
    redis_key = 'thepaper.cn:start_urls'
    allowed_domains = ['thepaper.cn']
    rules = [
        Rule(LinkExtractor(allow=('http://www.thepaper.cn/newsDetail_forward_\d+'),deny=()),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath('''//h1/text()''').extract()[0]
            content = ''.join(response.xpath('''//div[@class='news_txt']/text()''').extract())
            item['articleTitle'] = title
            item['articleUrl'] = ''.join(response.url)
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
