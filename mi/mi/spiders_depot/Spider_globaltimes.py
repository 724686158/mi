# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import jieba.analyse
class Spider_globaltimes(RedisCrawlSpider):
    name = 'globaltimes'
    redis_key = 'globaltimes:start_urls'
    allowed_domains = ['un.org']
    rules = [
        Rule(LinkExtractor(allow=('http://www.un.org/chinese/News/story.asp?NewsID=\w+'), deny=()),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath('''//div[@id='story-block']/h4X/text()''').extract()[0]
            print title
            content = ''.join(response.xpath(
                '''//div[@id='story-block']/div[@id='fullstory']/p/text()''').extract())
            print content
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

