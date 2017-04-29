# -*- coding: utf-8 -*-
import re
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from mi import settings as settings

class HuxiuSpider(RedisCrawlSpider):

    name = 'souhu'
    redis_key = settings.souhu_start_urls
    allowed_domains=['news.sohu.com']

    rules = (
        Rule(LinkExtractor(allow='http://news.sohu.com/\d{8}/\d*',deny=()),callback='processArticle',follow=True),
    )

    def processArticle(self,response):
        pattern = re.compile(r'\d+')
        try:
            articleId = pattern.findall(response.url)
            title = response.xpath("/html/body/div[@id='container']/div[@class='content-wrapper grid-675']/div[@class='content-box clear']/h1/text()").extract()[0]
            content = ''.join(response.xpath("/html/body/div[@id='container']/div[@class='content-wrapper grid-675']/div[@class='content-box clear']/div[@id='contentText']/div/p/text()").extract())
            item = ArticleItem()
            item['articleId'] = articleId
            item['articleTitle'] = title
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
