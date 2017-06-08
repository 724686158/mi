# -*- coding: utf-8 -*-
from goose import Goose
from goose.text import StopWordsChinese
from scrapy_redis.spiders import RedisCrawlSpider
from mi.items import ArticleItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from tools.fuzzyMatching import calc_score
class Spider_dezhoudailycom(RedisCrawlSpider):
    name = 'dezhoudaily.com'
    redis_key = 'dezhoudaily.com:start_urls'
    allowed_domains = ['dezhoudaily.com']
    rules = [
        Rule(LinkExtractor(allow=('dezhoudaily.com'),deny=()),callback='processArticle',follow=True)
    ]

    def processArticle(self,response):
        url = response.url
        score = calc_score(url)
        if score >= 3:
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
