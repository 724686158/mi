# -*- coding: utf-8 -*-
import json
def arr2str(arr):
    return ', '.join(map(lambda x: "'" + x + "'", arr))

#新闻类爬虫模板
spider_template = \
"""# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import jieba.analyse
class Spider_%s(RedisCrawlSpider):
    name = '%s'
    redis_key = '%s:start_urls'
    allowed_domains = [%s]
    rules = [
        Rule(LinkExtractor(allow=(%s),deny=(%s)),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath(''%s'').extract()[0]
            content = ''.join(response.xpath(''%s'').extract())
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

"""
def generate_spider(jsonfile):
    print jsonfile
    js = dict(json.loads(jsonfile))

    arr = (
        js['name'],
        js['name'],
        js['name'],
        arr2str(js['allowed_domains']),
        arr2str(js['rule_allow']),
        arr2str(js['rule_deny']),
        arr2str(js['xpath_title']),
        arr2str(js['xpath_content']))
    ok = spider_template % arr
    filename = "../spiders/" + 'spider_'+ js['name'] + '.py'
    with open(filename, 'w') as f:
        f.write(ok.encode('utf8'))