# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
class Spider_englishjs(RedisCrawlSpider):
    name = 'englishjs'
    redis_key = 'englishjs:start_urls'
    allowed_domains = ['english.jschina.com.cn']
    rules = [
        Rule(LinkExtractor(allow=('english.jschina.com.cn/\w+/\d{6}'),deny=()),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath('''//div[@class="doc"]/div[@id="title"]/text()''').extract()[0]
            content = ''.join(response.xpath('''//div[@class='TRS_Editor']/p/text()''').extract())
            item['articleTitle'] = title
            item['articleUrl'] = ''.join(response.url)
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
