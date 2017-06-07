# -*- coding: utf-8 -*-

import scrapy

# DOM树item
class DomTreeItem(scrapy.Item):
    # 文章的url
    url = scrapy.Field();
    # 文章的html
    html = scrapy.Field();

# 文章item，文章id用mongodb中自动生成的id来表示
class ArticleItem(scrapy.Item):
    # 文章标题
    articleTitle = scrapy.Field()
    # 文章url
    articleUrl = scrapy.Field()
    # 文章内容
    articleContent = scrapy.Field()
    # 文章关键词1
    articleFirstTag = scrapy.Field()
    # 文章关键词2
    articleSecondTag = scrapy.Field()
    # 文章关键词3
    articleThirdTag = scrapy.Field()

# 电商item，电商网站id在新建爬虫时自动生成
class ECommerce(scrapy.Field):
    # 电商网站名字
    eCommerceName = scrapy.Field()
    # 电商网站home页url
    eCommerceHomeUrl = scrapy.Field()

# 电商网站店家item
class ECommerceShopItem(scrapy.Field):
    # 电商网站名字
    eCommerceName = scrapy.Field()
    # 店家id
    shopId = scrapy.Field()
    # 店家名字
    shopName = scrapy.Field()
    # 店家链接
    shopUrl = scrapy.Field()
    # 店家所在地
    shopLocation=scrapy.Field()
    # 店家电话
    shopPhoneNumber=scrapy.Field()

# 电商网站店家评论item
class ECommerceShopCommentItem(scrapy.Field):
    # 电商网站名字
    eCommerceName = scrapy.Field()
    # 店家id
    shopId = scrapy.Field()
    # 店家评论页的链接
    shopCommentsUrl = scrapy.Field()
    # 店家评论数据
    shopCommentsData=scrapy.Field()

# 电商网站商品item
class ECommerceGoodItem(scrapy.Item):
    # 电商网站名字
    eCommerceName = scrapy.Field()
    # 商品id
    goodId = scrapy.Field()
    # 店家id
    shopId = scrapy.Field()
    # 商品名字
    goodName=scrapy.Field()
    # 商品链接
    goodUrl = scrapy.Field()
    # 商品价格
    goodPrice=scrapy.Field()

# 电商网站商品评论item
class ECommerceGoodCommentItem(scrapy.Item):
    # 电商网站名字
    eCommerceName = scrapy.Field()
    # 商品的id
    goodId=scrapy.Field()
    # 商品评论页的链接
    goodCommentsUrl=scrapy.Field()
    # 商品评论数据
    goodCommentsData=scrapy.Field()