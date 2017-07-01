#  -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from mi.items import ECommerceGoodItem
from mi.items import ECommerceGoodCommentItem
from mi.items import ECommerceShopCommentItem
from mi.items import ECommerceShopItem
import re
import requests

class Spider_gome(RedisCrawlSpider):

    name = 'gome.com.cn'
    redis_key = 'gome.com.cn:start_urls'
    allowed_domains = ['gome.com.cn']

    rules = {
        Rule(LinkExtractor(allow=('item.gome.com.cn'),deny=('image')),callback='processGood',follow=True)
    }

    priceUrlSegment1='https://ss.gome.com.cn/item/v1/d/m/store/'
    priceUrlSegment2='/'
    priceUrlSegment3='/N/11010200/110102002/null/flag/item/allStores?callback=allStores&_=1495607488107'

    # 获取商品信息
    def processGood(self,response):
        goodItem=ECommerceGoodItem()
        goodItem['eCommerceName'] = self.name
        try:
            title= response.xpath('''//div[@class='hgroup']/h1/text()''').extract()[0]
        except:
            print '无效页面'
            return
        pos = response.url.find('.html')
        url2 = response.url[24:pos]
        lis = url2.split('-')
        goodItem['goodId'] =lis[1]
        goodItem['goodName']=title
        goodItem['goodUrl']=response.url
        res=requests.get(url=self.priceUrlSegment1+lis[0]+self.priceUrlSegment2+lis[1]+self.priceUrlSegment3)
        pattern=re.compile(r'salePrice\":\"\d+')
        pattern2=re.compile(r'\d+')
        price=pattern2.findall(pattern.findall(res.content)[0])[0]
        goodItem['goodPrice'] = price

        #商品评论数据
        pattern4=re.compile(r'goodCommentPercent\":\"\d+')
        goodCommentPercent = pattern2.findall(pattern4.findall(res.content)[0])[0]

        pattern5 = re.compile(r'star\":\d+')
        star = pattern2.findall(pattern5.findall(res.content)[0])[0]

        pattern6=re.compile(r'comments\":\d+')
        comments = pattern2.findall(pattern6.findall(res.content)[0])[0]
        goodCommentsData={
            'goodCommentPercent':goodCommentPercent,
            'star':star,
            'comments':comments
        }

        goodCommentItem = ECommerceGoodCommentItem()
        goodCommentItem['eCommerceName'] = self.name
        goodCommentItem['goodId'] = lis[1]
        goodCommentItem['goodCommentsUrl']=''
        goodCommentItem['goodCommentsData']=str(goodCommentsData)
        yield goodCommentItem

        isGuomei = ''.join(
            response.xpath('''//div[@class='right']/div[@class='zy-stores']/span/text()''').extract())
        if isGuomei is '国美自营':
            goodItem['shopId'] = 'null'
        else:
            pattern3=re.compile(r'cn/\d+/?')
            shop = response.xpath('''//div[@class='ly-stores']/h2/a/@href''').extract()[0]
            shopId=pattern2.findall(pattern3.findall(shop)[0])[0]
            goodItem['shopId']=shopId
            yield goodItem

            shopName=response.xpath('''//div[@class='ly-stores']/h2/a/text() | //div[@class='zy-stores']/h2/a/text()''').extract()[0]

            shopData=''.join(response.xpath('''//div[@class='services-wrapper']/div[@class='services-stars']/span[@class='score']/text()''').extract()[0])

            shopItem=ECommerceShopItem()
            shopItem['eCommerceName'] = self.name
            shopItem['shopId']=shopId
            shopItem['shopName']=shopName
            shopItem['shopUrl']=shop
            shopItem['shopLocation']=''
            shopItem['shopPhoneNumber']=''
            yield shopItem

            shopCommentItem=ECommerceShopCommentItem()
            shopCommentItem['eCommerceName'] = self.name
            shopCommentItem['shopId']=shopId
            shopCommentItem['shopCommentsUrl']=''
            shopCommentItem['shopCommentsData']=shopData
            yield shopCommentItem

