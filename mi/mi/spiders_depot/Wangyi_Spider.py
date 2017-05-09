# -*- coding: utf-8 -*-
import re
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from mi import settings as settings

class WangyiSpider(RedisCrawlSpider):

    name = 'wangyi'
    redis_key = settings.wangyi_start_urls
    allowed_domains=['news.163.com']

    rules = (
        Rule(LinkExtractor(allow='http://news.163.com/\d{2}/\d{4}/\d{2}/*',deny=()),callback='processArticle',follow=True),
    )

    def processArticle(self,response):
        pattern = re.compile(r'\d+')
        try:
            articleId = pattern.findall(response.url)
            #
            title = response.xpath("/html[@id='ne_wrap']/body/div[@class='post_content post_area clearfix']/div[@id='epContentLeft']/h1/text() | /html/body/div[@class='blog-area']/div[@class='main-a clearfix']/div[@class='left']/h1/text()").extract()[0]
            content = ''.join(response.xpath("/html[@id='ne_wrap']/body/div[@class='post_content post_area clearfix']/div[@id='epContentLeft']/div[@class='post_body']/div[@id='endText']/p/text() | /html/body/div[@class='blog-area']/div[@class='main-a clearfix']/div[@class='left']/div[@id='main-content']/div[@id='endText']/p/text()").extract())
            item = ArticleItem()
            item['articleId'] = articleId
            item['articleTitle'] = title
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
