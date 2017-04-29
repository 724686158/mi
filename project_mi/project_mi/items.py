# -*- coding: utf-8 -*-
import scrapy

# models of scraped items
# 需爬取数据的模型

class ArticleItem(scrapy.Item):
    articleId=scrapy.Field()
    content=scrapy.Field()


