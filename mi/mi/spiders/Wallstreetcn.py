# -*- coding: utf-8 -*-
import re
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from mi import settings as settings

class HuaErJieSpider(RedisCrawlSpider):

    name = 'wallstreetcn'
    redis_key = settings.huaerjie_start_urls
    allowed_domains = ['wallstreetcn.com']

    rules = [
        Rule(LinkExtractor(allow=('https://wallstreetcn.com/articles/'),deny=()),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        pattern = re.compile(r'\d+')
        try:
            articleId = pattern.findall(response.url)

            title = response.xpath("/html/body/div[@id='app']/div[@class='layout-main']/main/div[@class='article-wrapper']/div[@class='article main-article']/div[@class='article__heading']/div[@class='article__heading__title']/text()").extract()[0]
            content = ''.join(response.xpath('//div[@class="article__content"]/div[@class="node-article-content"]//p/text()').extract())

            item = ArticleItem()
            item['articleId'] = articleId
            item['articleContent'] = content
            item['articleTitle'] = title
            yield item
        except:
            self.logger.info('item in article failed')
