# -*- coding: utf-8 -*-

import scrapy

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

    # 以下三个数据在程序开始时进行预处理，通过配置文件的形式手动存入数据库

class ECommerce(scrapy.Field):
    # 电商网站Id
    eCommerceId = scrapy.Field()
    # 电商网站名字
    eCommerceName = scrapy.Field()
    # 电商网站home页url
    eCommerceHomeUrl = scrapy.Field()

class ECommerceShopItem(scrapy.Field):
    # 店家id
    shopId = scrapy.Field()
    # 电商网站Id
    eCommerceId = scrapy.Field()
    # 店家名字
    shopName = scrapy.Field()
    # 店家链接
    shopUrl = scrapy.Field()
    # 店家所在地
    shopLocation=scrapy.Field()
    # 店家电话
    shopPhoneNumber=scrapy.Field()

class ECommerceShopCommentItem(scrapy.Field):
    # 店家id
    shopId = scrapy.Field()
    # 店家总评
    shopTotalRating = scrapy.Field()
    # 总评相对于行业其他店家
    shopTotalRatingCTC = scrapy.Field()
    # 店家商品质量满意度
    shopGoodQualitySatisficationRating = scrapy.Field()
    # 店家商品质量满意度相对于行业其他店家
    shopGoodQualitySatisficationRatingCTC = scrapy.Field()
    # 店家服务满意度
    shopServiceSatisficationRating = scrapy.Field()
    # 店家服务满意度相对于行业其他店家
    shopServiceSatisficationRatingCTC = scrapy.Field()
    # 店家物流速度满意度
    shopLogisticsSpeedSatisficationRating = scrapy.Field()
    # 店家物流速度满意度相对于行业其他店家
    shopLogisticsSpeedSatisficationRatingCTC = scrapy.Field()
    # 商品描述满意度
    shopGoodDescriptionSatisficationRating = scrapy.Field()
    # 商品描述满意度相对于行业其他店家
    shopGoodDescriptionSatisficationRatingCTC = scrapy.Field()
    # 处理退换货满意度
    shopProcessingReturnAndExchangeGoodSatisficationRating = scrapy.Field()
    # 处理退换货满意度相对于行业其他店家
    shopProcessingReturnAndExchangeGoodSatisficationRatingCTC = scrapy.Field()
    # 店家违规次数
    shopDisobeyRulesTimes = scrapy.Field()


class ECommerceGoodItem(scrapy.Item):
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

class ECommerceGoodCommentItem(scrapy.Item):
    # 商品的id
    goodId=scrapy.Field()
    # 商品被评论的数量
    goodCommentsCount=scrapy.Field()
    # 商品评论页的链接
    goodCommentsUrl=scrapy.Field()
    # 商品晒单数量
    goodDisplayPictureCount = scrapy.Field()
    # 商品追加评论数量
    goodAddCommentCount = scrapy.Field()
    # 商品好评数量
    goodRankBetterCommentCount = scrapy.Field()
    # 商品中评数量
    goodRankMediateCommentCount = scrapy.Field()
    # 商品差评数量
    goodRankWorseCommentCount = scrapy.Field()

