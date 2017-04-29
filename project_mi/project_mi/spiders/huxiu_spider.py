# -*- coding:utf-8 -*-
import re
import scrapy

from scrapy_redis.spiders import RedisSpider

import project_mi.items


class RedisTestSpider(RedisSpider):

    name = "huxiu"
    redis_key = "huxiu:start_urls"
    huxiuBaseUrl = 'https://www.huxiu.com'
    channelHref=set()
    tagsHasBeenCrawled=False
    tags=set()

    def parse(self, response):

        channelsHrefs=response.xpath('//div[@class="container"]/ul[@class="nav navbar-nav navbar-left"]/li[@class="nav-news js-show-menu"]/ul[@class="header-column header-column1 header-column-zx menu-box"]/li/a/@href').extract()
        for href in channelsHrefs:
            href=self.huxiuBaseUrl+href
            self.channelHref.add(href)
        for href in self.channelHref:
            yield scrapy.Request(url=href, callback=self.processChannel)

        #yield scrapy.Request(url='https://www.huxiu.com/collection/1.html',callback=)
        #yield scrapy.Request(url='https://www.huxiu.com/collection/2.html', callback=)

        #yield scrapy.Request(url='https://www.huxiu.com/article/188302.html',callback=self.processArticel)

        #yield scrapy.Request(url='https://www.huxiu.com/tags',callback=self.processTagsPage)

    def processChannel(self,response):

        topArticles=[]

        hotArticles=[]

        specials=[]

        authors=[]

        try:
            topArticlesHrefs=response.xpath('//div[@class="container"]/div[@class="wrap-left pull-left"]/div[@class="mod-info-flow"]/div[@class="mod-b mod-art "]/div[@class="mob-ctt"]/h2/a[@class="transition msubstr-row2"]/@href').extract()
            for href in topArticlesHrefs:
                topArticles.append(self.huxiuBaseUrl+href)
            try:
                for href in topArticles:
                    yield scrapy.Request(url=href,callback=self.processArticel)
            except:
                self.logger.info('topArticlesHrefs failed')
        except:
            self.logger.info('topArticles failed')

        try:
            hotArticlesHrefs=response.xpath('//div[@class="wrap-right pull-right"]/div[@class="box-moder hot-article"]/ul/li/a[@class="transition"]/@href').extract()
            for href in hotArticlesHrefs:
                hotArticles.append(self.huxiuBaseUrl+href)

            try:
                for href in hotArticles:
                    yield scrapy.Request(url=href,callback=self.processArticel)
            except:
                self.logger.info('hotArticlesHrefs failed')
        except:
            self.logger.info('hotArticles failed')


        try:
            authorsHrefs=response.xpath('//div[@class="container"]/div[@class="wrap-left pull-left"]/div[@class="mod-info-flow"]/div[@class="mod-b mod-art "]/div[@class="mob-ctt"]/div[@class="mob-author"]/div[@class="author-face"]/a/@href').extract()
            for href in authorsHrefs:
                if 'member' in href:
                    authors.append(self.huxiuBaseUrl+href)

            try:
                for href in authors:
                    yield scrapy.Request(url=href,callback=self.processAuthor)
            except:
                self.logger.info('authorsHrefs failed')
        except:
            self.logger.info('authors failed')

        try:
            specialsHrefs=response.xpath('//div[@class="zt-article"]/ul/li/a/@href').extract()
            for href in specialsHrefs:
                specials.append(self.huxiuBaseUrl+href)
            try:
                for href in specials:
                    yield scrapy.Request(url=href,callback=self.processSpecial)
            except:
                self.logger.info('specialsHrefs failed')
        except:
            self.logger.info('specials failed')

    def processArticel(self,response):
        pattern=re.compile(r'\d+')
        try:
            articleId=pattern.findall(response.url)
            contentId='article_content'+str(articleId)
            content=''.join(response.xpath('//div[@class="article-content-wrap"]//p/text()').extract())

            item=project_mi.items.ArticleItem()
            item['articleId']=articleId
            item['content']=content
            yield item
        except:
            self.logger.info('item in article failed')
        hotArticles=[]
        try:
            hotArticlesHrefs=response.xpath('//div[@class="box-moder hot-article"]/ul/li/a/@href').extract()
            for href in hotArticlesHrefs:
                hotArticles.append(self.huxiuBaseUrl+href)
            try:
                for href in hotArticles:
                    yield scrapy.Request(url=href,callback=self.processArticel)
            except:
                self.logger.info('hotArticlesHrefs in article failed')
        except:
            self.logger.info('hotArticles in article failed')


        currentTags=[]

        try:
            tagsHrefs=response.xpath('//div[@class="box-moder hot-tag"]/div[@class="search-history search-hot"]/ul/li/a/@href').extract()
            for href in tagsHrefs:
                if self.huxiuBaseUrl+href not in self.tags:
                    self.tags.add(self.huxiuBaseUrl+href)
                    currentTags.append(self.huxiuBaseUrl+href)
            try:
                for href in currentTags:
                    yield scrapy.Request(url=href,callback=self.processSingleTagPage)
            except:
                self.logger.info('tagsHrefs in article failed')

        except:
            self.logger.info('hot tags in article failed')

    def processTagsPage(self,response):
        try:
            tagsHrefs=response.xpath('//div[@class="tag-wrap"]//div[@class="tag-cnt-box"]//div[@class="search-history"]//li[@class="transition"]/a/@href').extract()
            for tagsHref in tagsHrefs:
                print self.huxiuBaseUrl+tagsHref
                self.tags.add(self.huxiuBaseUrl+tagsHref)
            try:
                for tagHref in self.tags:
                    yield scrapy.Request(url=tagHref,callback=self.processSingleTagPage)
            except:
                self.logger.info('tagRequest failed')
        except:
            self.logger.info('tags failed')

    def processSingleTagPage(self,response):
        try:
            articles=response.xpath('//div[@class="related-article"]//li/a/@href').extract()
            articleHrefs=[]
            for href in articles:
                print self.huxiuBaseUrl+href
                articleHrefs.append(self.huxiuBaseUrl+href)
            try:
                for href in articleHrefs:
                    yield scrapy.Request(url=href,callback=self.processArticel)
            except:
                self.logger.info('article acquire failed in single tag')
        except:
            self.logger.info('single tag page failed')

    def processAuthor(self,response):

        articles=[]
        try:
            articleHrefs=response.xpath('//div[@class="message-box"]//div[@class="mod-b mod-art "]/a[@class="mod-b mod-art "]/@href').extract()
            for href in articleHrefs:
                print self.huxiuBaseUrl+href
                articles.append(self.huxiuBaseUrl+href)
            try:
                for href in articles:
                    yield scrapy.Request(url=href,callback=self.processArticel)
            except:
                self.logger.info('article in processAuthor failed')
        except:
            self.logger.info('processAuthor failed')

        nextHref=[]
        nextUrlEnd=response.xpath('//div[user-content-warp]/div[@class="message-box"]/nav[@class="page-nav"]/ul/li[@class="disabled"]').extract()
        if nextUrlEnd is not None:
            nextHrefs=response.xpath('//div[user-content-warp]/div[@class="message-box"]/nav[@class="page-nav"]/ul/li/a/@href').extract()
            for href in nextHrefs:
                if '#' not in href:
                    nextHref.append(self.huxiuBaseUrl+href)
                    print self.huxiuBaseUrl+href
            try:
                for href in nextHref:
                    yield scrapy.Request(url=href,callback=self.processAuthor)
            except:
                self.logger.info('next href in processAuthor failed')

    def processSpecial(self,response):

        specialArticles=[]
        try:
            specialArticlesHrefs=response.xpath('//div[@class="mod-info-flow"]/div[@class="zt-article-box"]//div[@class="mod-b mod-art "]/div[@class="mob-ctt"]/h2/a/@href').extract()
            for href in specialArticlesHrefs:
                print self.huxiuBaseUrl+href
                specialArticles.append(self.huxiuBaseUrl+href)
            try:
                for href in specialArticles:
                    yield scrapy.Request(url=href,callback=self.processArticel)
            except:
                self.logger.info('process article in processSpecial')
        except:
            self.logger.info('processSpecial failed')
