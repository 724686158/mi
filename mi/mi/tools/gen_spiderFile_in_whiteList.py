# -*- coding: utf-8 -*-
import os
def arr2str(arr):
    return ', '.join(map(lambda x: "'" + x + "'", arr))

#新闻类爬虫模板
spider_template = \
"""# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
class Spider_%s(RedisCrawlSpider):
    name = '%s'
    redis_key = '%s:start_urls'
    allowed_domains = [%s]
    rules = [
        Rule(LinkExtractor(allow=(%s),deny=()),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        try:
            item = ArticleItem()
            title = response.xpath(''%s'').extract()[0]
            content = ''.join(response.xpath(''%s'').extract())
            item['articleTitle'] = title
            item['articleUrl'] = ''.join(response.url)
            item['articleContent'] = content
            yield item
        except:
            self.logger.info('item in article failed')
"""
# 传入字典格式的字符串
def generate_spider(spidername, jsonfile):
    try:
        dic = eval(jsonfile)
        arr = (
            spidername.split('.')[0],
            spidername,
            spidername,
            arr2str(dic['allowed_domains']),
            arr2str(dic['rule_allow']),
            arr2str(dic['xpath_title']),
            arr2str(dic['xpath_content']))
        ok = spider_template % arr
        filename = os.getcwd() + '/mi/spiders_of_news_in_whiteList/spider_'+ spidername.replace('.', '')  + '.py'
        with open(filename, 'w') as f:
            f.write(ok.encode('utf8'))
            print 'success'
        return True
    except:
        print 'fall'
        return False
    finally:
        f.close()