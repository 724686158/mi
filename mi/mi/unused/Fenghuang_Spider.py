import re
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from mi import settings as settings

class FenghuangSpider(RedisCrawlSpider):

    name = 'fenghuang'
    redis_key = settings.fenghuang_start_urls
    allowed_domains=['http://news.ifeng.com']

    rules = (
        Rule(LinkExtractor(allow='news.ifeng.com/a/\d{8}/\d*'),callback='processArticle',follow=True),
    )
    def processArticle(self,response):
        pattern = re.compile(r'\d+')
        try:
            articleId = pattern.findall(response.url)
            title = response.xpath('/html/body/div[@class="main"]/div[@class="left"]/div[@id="artical"]/h1[@id="artical_topic"]')
            content = ''.join(response.xpath('/html/body/div[@class="main"]/div[@class="left"]/div[@id="artical"]/div[@id="artical_real"]/div[@id="main_content"]'))
            item = ArticleItem()
            item['articleId'] = articleId
            item['articleTitle'] = title
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
