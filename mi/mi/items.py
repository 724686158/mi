# -*- coding: utf-8 -*-

import scrapy

class ArticleItem(scrapy.Item):
    articleId=scrapy.Field()
    articleTitle = scrapy.Field()
    articleContent = scrapy.Field()