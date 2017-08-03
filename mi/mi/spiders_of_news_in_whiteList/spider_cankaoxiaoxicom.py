# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
class Spider_cankaoxiaoxi(RedisCrawlSpider):
    name = 'cankaoxiaoxi.com'
    redis_key = 'cankaoxiaoxi.com:start_urls'
    allowed_domains = ['cankaoxiaoxi.com']
    rules = [
        Rule(LinkExtractor(allow=('cankaoxiaoxi.com/\w+/\d{8}'),deny=()),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath('''//div[@class="column"]//div[@class="bg-content"]/h1/text()''').extract()[0]
            content = ''.join(response.xpath('''//div[@class='inner']/div[@class="fs-small cont-detail det article-content ov"]/p/text()''').extract())
            item['articleTitle'] = title
            item['articleUrl'] = ''.join(response.url)
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
