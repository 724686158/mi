# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import jieba.analyse
class Spider_taiwan(RedisCrawlSpider):
    name = 'taiwan'
    redis_key = 'taiwan:start_urls'
    allowed_domains = ['eng.taiwan.cn']
    rules = [
        Rule(LinkExtractor(allow=('eng.taiwan.cn/\w+/\d{6}'),deny=()),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath('''//div[@class='en_line2_2left_2']/div[@class="en_text"]/h1/text()''').extract()[0]
            content = ''.join(response.xpath('''//div[@class='fontsizebox']/div[@class="TRS_Editor"]/p/text()''').extract())
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
