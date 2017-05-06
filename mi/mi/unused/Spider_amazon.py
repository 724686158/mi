#  -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule

from scrapy.linkextractors import LinkExtractor
from mi.items import ECommerceGoodItem
from mi.items import ECommerceGoodCommentItem
from mi.items import ECommerceShopCommentItem
from mi.items import ECommerceShopItem
import re
import requests
import json
class AmazonSpider(RedisCrawlSpider):

    name = 'amazon'
    redis_key = 'amazon:start_urls'
    allowed_domains = ['amazon.cn']

    rules = {
        Rule(LinkExtractor(allow=('.*//www.amazon.cn/gp/product/.*','.*//www.amazon.cn/dp/.*','.*//www.amazon.cn/.*/dp.*'), deny=()),callback='processGood',follow=True),
        Rule(LinkExtractor(allow=('.*//www.amazon.cn/gp/aag/main?.*'), deny=()), callback='processShop', follow=True)
    }

    # 电商Id
    eCommerceId = 2

    # 获取商品信息
    def processGood(self,response):
        goodId = ''
        try:
            if 'gp/product' in response.url:
                idPattern = re.compile(r'product/\d|\w{10}')
                goodId = idPattern.findall(response.url)[0]
                goodId = str(goodId).strip('product').strip('/')
            elif 'dp' in response.url:
                idPattern = re.compile(r'dp/\d|\w{10}')
                goodId = idPattern.findall(response.url)[0]
                goodId = str(goodId).strip('dp').strip('/')
        except:
            print '无效的商品页'
        goodItem = ECommerceGoodItem()
        goodItem['eCommerceId'] = self.eCommerceId
        goodItem['goodId'] = goodId
        shopIdPattern = re.compile(r'seller=\d|\w{13,14}')
        try:
            shopMessage = ''.join(response.xpath('//div[@id="dynamicDeliveryMessage_feature_div"]//span[@id="ddmMerchantMessage"]/a/text()').extract())
            shopName = shopMessage
            shopUrl = 'https://www.amazon.cn' + response.xpath('//div[@id="dynamicDeliveryMessage_feature_div"]//span[@id="ddmMerchantMessage"]/a/@href').extract()[0]
            shopIdPattern = re.compile(r'seller=\d|\w{13,14}&')
            shopId = shopIdPattern.findall(shopUrl)[0].strip('seller=').strip('&')
            goodItem['shopId'] = shopId
            # 直接发一个获取店家信息的Request
            yield scrapy.Request(url=shopUrl, callback=self.processShopItem,
                                 meta={'shopName': shopName, 'shopUrl': shopUrl, 'shopId': shopId})
        except:
            goodItem['shopId'] = "自营"
        name = ''.join(response.xpath('//div[@class="a-container"]/div[@id="centerCol"]/div[@id="title_feature_div"]/div[@id="titleSection"]/h1[@id="title"]/span[@id="productTitle"]/text()').extract()).strip()
        goodItem['goodName'] = name
        goodItem['goodUrl'] = response.url
        try:
            price=''.join(response.xpath('//div[@id="price_feature_div"]//span[@id="priceblock_ourprice"]/text()').extract())
            if price is not '':
                goodItem['goodPrice'] = price
            elif price is '':
                price=''.join(response.xpath('//div[@id="price_feature_div"]/div[@id="priceblock_saleprice"]/text()').extract())
                if price is not '':
                    goodItem['goodPrice'] = price
                elif price is '':
                    goodItem['goodPrice'] = '无货'
        except:
            goodItem['goodPrice']='无货'
        yield goodItem

        goodCommentItem=ECommerceGoodCommentItem()
        goodCommentItem['eCommerceId'] = self.eCommerceId
        goodCommentItem['goodId'] = goodId
        try:
            goodCommentUrl=response.xpath('//div[@id="summaryStars"]/a[@class="a-link-normal a-text-normal product-reviews-link"]/@href').extract()[0]
            goodCommentStar=''.join(response.xpath('//div[@id="summaryStars"]//span[@class="a-icon-alt"]/text()').extract())
            goodCommentItem['goodCommentsUrl']=goodCommentUrl
            goodCommentItem['goodCommentsData']=goodCommentStar
        except:
            goodCommentItem['goodCommentsUrl'] = '无评论链接'
            goodCommentItem['goodCommentsData'] = '无评论数据'
        yield goodCommentItem

    # 获取店家信息
    def processShop(self,response):
        print "获取店家信息"
        shopItem = ECommerceShopItem()
        shopItem['eCommerceId'] = self.eCommerceId
        shopItem['shopId'] = response.meta['shopId']
        shopItem['shopName']=response.meta['shopName']
        shopItem['shopUrl'] = response.meta['shopUrl']
        shopInfoLi=response.xpath('//div[@class="blueBorder aag_legalinfo"]//li[@class="aagLegalRow"]')
        location=''.join(shopInfoLi[0].xpath('./text()').extract()).strip()
        phoneNumber=''.join(shopInfoLi[1].xpath('./text()').extract()).strip()
        shopItem['shopLocation'] = location
        shopItem['shopPhoneNumber'] = phoneNumber
        yield shopItem

        shopCommentItem=ECommerceShopCommentItem()
        shopCommentItem['eCommerceId'] = self.eCommerceId
        shopCommentItem['shopId'] = response.meta['shopId']
        shopCommentItem['shopCommentsUrl'] = response.url
        shopCommentItem['shopCommentsData']=''.join(response.xpath('//div[@class="starRating"]/span/span/text()').extract())
        yield shopCommentItem


