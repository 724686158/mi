# -*- coding: utf-8 -*-
import re
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from mi import settings as settings

class HuxiuSpider(RedisCrawlSpider):

    name = 'huxiu'
    redis_key = settings.huxiu_start_urls
    allowed_domains=['huxiu.com']

    rules = (
        Rule(LinkExtractor(allow='https://www.huxiu.com/article/',deny=()),callback='processArticle',follow=True),
    )

    def processArticle(self,response):
        pattern = re.compile(r'\d+')
        try:
            articleId = pattern.findall(response.url)
            title = response.xpath("//div[@class='article-wrap']/h1[@class='t-h1']/text()").extract()[0]
            content = ''.join(response.xpath("//div[@class='article-content-wrap']//p/text()").extract())
            item = ArticleItem()
            item['articleId'] = articleId
            item['articleTitle'] = title
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
