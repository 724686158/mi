#  -*- coding: utf-8 -*-
import scrapy
import re
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from mi.items import ECommerceGoodItem
from mi.items import ECommerceGoodCommentItem
from mi.items import ECommerceShopCommentItem
from mi.items import ECommerceShopItem

class Spider_dangdang(RedisCrawlSpider):

    name = 'dangdang.com'
    redis_key = 'dangdang.com:start_urls'
    allowed_domains = ['dangdang.com']

    rules = {
        Rule(LinkExtractor(allow=('product.dangdang.com/\d+'), deny=()),callback='processGood',follow=True),
        Rule(LinkExtractor(allow=('shop.dangdang.com/\d+'), deny=()) ,follow=True),
        Rule(LinkExtractor(allow=('category.dangdang.com/cid\d+'),deny=()),callback='processSearchPage' ,follow=True)
    }

    # 获取商品信息
    def processGood(self,response):
        try:
            pattern = re.compile(r'\d+')
            itemId = pattern.findall(response.url)[0]
        except:
            print '无效的商品页'
        else:
            # 商品信息
            goodItem = ECommerceGoodItem()
            goodItem['eCommerceName'] = self.name

            goodItem['goodId'] = itemId
            title=response.xpath('''//div[@class='name_info']/h1/text()''').extract()[0].strip()
            goodItem['goodName']=title
            try:
                shopId=response.xpath('''//div[@class='service_more_info']/p[@class='title clearfix']//a/@href''').extract()[0]
                shopId=pattern.findall(shopId)[0]
                goodItem['shopId']=shopId
            except:
                goodItem['shopId']='null'#自营
            goodItem['goodUrl']=response.url

            goodPrice=response.xpath('''//p[@id='dd-price']/text()''').extract()[0]
            goodItem['goodPrice']=goodPrice
            yield goodItem
            goodCommentItem=ECommerceGoodCommentItem()
            goodCommentItem['eCommerceName'] = self.name
            goodCommentItem['goodId']=itemId
            goodCommentsData=''.join(response.xpath('''//div[@class='pinglun']/a[@id='comm_num_down']/text()''').extract())
            goodCommentsUrl=response.url+'?point=comment_point'
            goodCommentItem['goodCommentsUrl']=goodCommentsUrl
            goodCommentItem['goodCommentsData']=goodCommentsData

            yield goodCommentItem
            if goodItem['shopId'] != 'null':
                print goodItem['shopId']
                shopItem = ECommerceShopItem()
                shopItem['eCommerceName'] = self.name
                shopItem['shopId'] = goodItem['shopId']
                shopName = ''.join(response.xpath('''//div[@class='service_more_info']/p[@class='title clearfix']//a/text()''').extract())
                shopItem['shopName']=shopName
                shopUrl=response.xpath('''//div[@class='service_more_info']/p[@class='title clearfix']//a/@href''').extract()[0]
                shopItem['shopUrl']=shopUrl
                shopItem['shopLocation']=''
                shopItem['shopPhoneNumber']=''
                yield scrapy.Request(url=shopUrl, callback=self.processShop, meta={'shopItem': shopItem})

    def processShop(self,response):
        shopCommentItem = ECommerceShopCommentItem()
        shopCommentItem['eCommerceName'] = self.name
        shopCommentItem['shopId'] = response.meta['shopItem']['shopId']
        shopCommentItem['shopCommentsUrl'] = ''
        shopCommentItem['shopCommentsData'] = ''
        yield response.meta['shopItem']
        yield shopCommentItem












