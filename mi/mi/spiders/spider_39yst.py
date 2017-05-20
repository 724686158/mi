# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import jieba.analyse
class Spider_39yst(RedisCrawlSpider):
    name = '39yst'
    redis_key = '39yst:start_urls'
    allowed_domains = ['39yst.com']
    rules = [
        Rule(LinkExtractor(allow=('39yst.com/\w+/\w+/\d+', '39yst.com/\w+/\d+'),deny=()),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath('''//div[@class='articlewrap']/h1/text()''').extract()[0]
            content = ''.join(response.xpath('''//div[@id='articleContent']/p/text()''').extract())
            item['articleTitle'] = title
            item['articleUrl'] = ''.join(response.url)
            item['articleContent'] = content
            tags = jieba.analyse.extract_tags(content, topK=20, withWeight=5)
            item['articleFirstTag'] = ''.join(tags[0][0])
            item['articleSecondTag'] = ''.join(tags[1][0])
            item['articleThirdTag'] = ''.join(tags[2][0])
            yield item
        except:
            self.logger.info('item in article failed')
