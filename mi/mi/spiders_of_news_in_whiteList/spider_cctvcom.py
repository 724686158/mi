# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
class Spider_cctv(RedisCrawlSpider):
    name = 'cctv.com'
    redis_key = 'cctv.com:start_urls'
    allowed_domains = ['english.cctv.com']
    rules = [
        Rule(LinkExtractor(allow=('english.cctv.com/\d{4}/\d{2}/\d{2}'),deny=()),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath('''//div[@id="jh604"]/div[@class="guojiA10232_ind03"]/h3/text()''').extract()[0]
            content = ''.join(response.xpath('''//div[@class='text']/p/text()''').extract())
            item['articleTitle'] = title
            item['articleUrl'] = ''.join(response.url)
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
