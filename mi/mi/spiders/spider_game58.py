# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
class Spider_game58(RedisCrawlSpider):
    name = 'game58'
    redis_key = 'game58:start_urls'
    allowed_domains = ['58game.com']
    rules = [
        Rule(LinkExtractor(allow=('58game.com/\w+/article-\d+'),deny=()),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath('''//div[@class="news-title-v3"]/h4/text()''').extract()[0]
            content = ''.join(response.xpath('''//div[@class='content-area-v3']/p/text()''').extract())
            item['articleTitle'] = title
            item['articleUrl'] = ''.join(response.url)
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
