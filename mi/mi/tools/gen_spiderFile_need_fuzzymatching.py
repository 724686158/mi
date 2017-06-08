# -*- coding: utf-8 -*-
import os
# 模糊匹配时相信是新闻正文页的分值
score = 3
# 新闻爬虫(模糊匹配)模板
spider_template = \
"""# -*- coding: utf-8 -*-
from goose import Goose
from goose.text import StopWordsChinese
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from tools.fuzzyMatching import calc_score
class Spider_%s(RedisCrawlSpider):
    name = '%s'
    redis_key = '%s:start_urls'
    allowed_domains = ['%s']
    rules = [
        Rule(LinkExtractor(allow=('%s'),deny=()),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        url = response.url
        score = calc_score(url)
        if score >= %s:
            try:
                print 'this url maybe a news_url'
                item = ArticleItem()
                g = Goose()
                article = g.extract(url = url)
                title = article.title
                content = article.cleaned_text
                if len(content) == 0:
                    print 'news in chinese'
                    g = Goose({'stopwords_class': StopWordsChinese})
                    article = g.extract(url=url)
                    content = article.cleaned_text
                item['articleTitle'] = title
                item['articleUrl'] = url
                item['articleContent'] = content
                yield item
            except:
                self.logger.info('item in article failed')

        else:
            print 'this url maybe not a news_url, ' + ' score only ' + str(score)
            print 'you can check this url: ' + url
            return
"""
# 传入字典格式的字符串
def generate_spider(spidername):

    try:
        arr = (
        str(spidername).replace('.', ''),
        spidername,
        spidername,
        spidername,
        spidername,
        str(score))
        ok = spider_template % arr
        filename = os.getcwd() + '/mi/spiders_of_news_need_fuzzymatching/spider_' + spidername.replace('.', '') + '.py'
        with open(filename, 'w') as f:
            f.write(ok.encode('utf8'))
            return True
    except:
        return False
    finally:
        f.close()