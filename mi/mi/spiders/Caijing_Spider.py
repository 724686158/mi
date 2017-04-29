# -*- coding: utf-8 -*-
import re
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from mi import settings as settings

class CaiJingWangSpider(RedisCrawlSpider):

    name = 'caijing'
    redis_key = settings.caijing_start_urls
    allowed_domains = ['caijing.com.cn']

    rules = [
        Rule(LinkExtractor(allow=('caijing.com.cn/\d{8}/\d*'),deny=('.*photos.*', '.*politics.*')),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        pattern = re.compile(r'\d+')
        try:
            articleId = pattern.findall(response.url)
            title = response.xpath(
                "/html/body/div[@class='center']/div[@class='content']/div[@class='main']/div[@class='main_lt article_lt']/div[@id='article']/h2[@id='cont_title']/text()").extract()[0]
            content = ''.join(response.xpath('//div[@class="article-content"]//p/text()').extract())
            item = ArticleItem()
            item['articleId'] = articleId
            item['articleTitle'] = title
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')



