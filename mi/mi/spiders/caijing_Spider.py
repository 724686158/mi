# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import jieba.analyse
class Spider_caijing(RedisCrawlSpider):
    name = 'caijing'
    redis_key = 'caijing_start_urls'
    allowed_domains = ['caijing.com.cn']
    rules = [
        Rule(LinkExtractor(allow=('caijing.com.cn/\d{8}/\d*'),deny=('.*photos.*', '.*politics.*')),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath('''/html/body/div[@class='center']/div[@class='content']/div/div/div[@id='article']/h2/text()''').extract()[0]
            content = ''.join(response.xpath('''/html/body/div[@class='center']/div[@class='content']/div[@class='main']/div/div[@id='article']/div[@id='the_content']/p/text()''').extract())
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

