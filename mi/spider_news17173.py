# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import jieba.analyse
class Spider_news17173(RedisCrawlSpider):
    name = 'news17173'
    redis_key = 'news17173:start_urls'
    allowed_domains = ['news.17173.com']
    rules = [
        Rule(LinkExtractor(allow=('news.17173.com/content/\d+'),deny=('')),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath('''//h1[@class="gb-final-tit-article"]/text()''').extract()[0]
            content = ''.join(response.xpath('''//div[@class='gb-final-mod-article gb-final-mod-article-p2em']/p/text()''').extract())
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
