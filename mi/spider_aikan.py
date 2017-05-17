# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import jieba.analyse
class Spider_aikan(RedisCrawlSpider):
    name = 'aikan'
    redis_key = 'aikan:start_urls'
    allowed_domains = ['aikanxinwen.com']
    rules = [
        Rule(LinkExtractor(allow=('aikanxinwen.com/view/'),deny=('')),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath('''//header[@class='article-header']/h1/text()''').extract()[0]
            content = ''.join(response.xpath('''//article[@class='article-content article-ar-content']/p/text()''').extract())
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
