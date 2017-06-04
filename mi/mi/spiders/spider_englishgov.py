# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
class Spider_englishgov(RedisCrawlSpider):
    name = 'englishgov'
    redis_key = 'englishgov:start_urls'
    allowed_domains = ['english.gov.cn']
    rules = [
        Rule(LinkExtractor(allow=('english.gov.cn/news/\w+/\d{4}/\d{2}/\d{2}/content'),deny=()),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath('''//div[@class='content-left']/div[@class="conter-conter"]/h3/text()''').extract()[0]
            content = ''.join(response.xpath('''//div[@id='sp']//p/text()''').extract())
            item['articleTitle'] = title
            item['articleUrl'] = ''.join(response.url)
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
