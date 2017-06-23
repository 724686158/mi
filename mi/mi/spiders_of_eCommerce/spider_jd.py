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
import json

class Spider_jd(RedisCrawlSpider):

    name = 'jd.com'
    redis_key = 'jd.com:start_urls'
    allowed_domains = ['jd.com']

    rules = {
        Rule(LinkExtractor(allow=('https://item.jd.com/\d+.html'), deny=()),callback='processGood',follow=True),
        Rule(LinkExtractor(allow=('https://mall.jd.com/shopLevel-\d+.html'), deny=()) ,callback= 'processShop',follow=True),
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
            try:
                shopCommentUrl = response.xpath('''//div[@class='aside']/div[@class='m m-aside popbox']/div[@class='popbox-inner']/div[@class='mc']/div[@class='pop-score-summary']/a/@href''').extract()[0]
                shopId = pattern.findall(shopCommentUrl)[0]
                goodItem['shopId'] = shopId
            except:
                #自营等无法获取店家id的情况
                goodItem['shopId'] = 0
            goodItem['goodName'] = ''.join(response.xpath('''//div[@class='itemInfo-wrap']/div[@class='sku-name']/text()''').extract()).strip()
            goodItem['goodUrl'] = response.url
            try:
                priceResponse = requests.get(url='https://p.3.cn/prices/mgets?&pduid=1&skuIds=J_' + str(itemId)).text
                data = json.loads(priceResponse)[0]
                itemPrice = data['p']
                goodItem['goodPrice'] = itemPrice
            except:
                goodItem['goodPrice'] = '无货'
            yield goodItem

            # 商品评论信息
            commentItem = ECommerceGoodCommentItem()
            commentItem['eCommerceName'] = self.name
            commentItem['goodId'] = itemId
            commentDict={'productId':str(itemId), 'score':'0','sortType':'5','page':'0','pageSize':'10','isShadowSku':'0'}
            queryCommentsDataUrl='https://club.jd.com/comment/productPageComments.action?'+'productId='+commentDict['productId']+'&score='+commentDict['score']+'&sortType='+commentDict['sortType']+'&page='+commentDict['page']+'&pageSize='+commentDict['pageSize']+'&isShadowSku='+commentDict['isShadowSku']
            commentItem['goodCommentsUrl'] = queryCommentsDataUrl
            content = json.loads(requests.get(queryCommentsDataUrl).content.decode('gbk', 'ignore').encode('utf-8'))
            commentsData=content['productCommentSummary']
            commentItem['goodCommentsData'] = str(commentsData)
            yield commentItem

    # 获取店家信息
    def processShop(self,response):
        try:
            pattern = re.compile(r'\d+')
            shopId = pattern.findall(response.url)[0]
        except:
            print '无效的店家页'
        else:
            # 店家信息
            shopItem=ECommerceShopItem()
            shopItem['eCommerceName'] = self.name
            shopItem['shopId']=shopId
            shopItem['shopName'] = ''.join(response.xpath('''/html/body[@id='pop']/div[@class='forBack']/div[@id='wrap']/div[@class='j-rating-content']/div[@class='j-shop-info']/p[@class='j-shop-name']/text()''').extract()).strip()
            shopItem['shopLocation'] = ''.join(response.xpath('''/html/body[@id='pop']/div[@class='forBack']/div[@id='wrap']/div[@class='j-rating-content']/div[@class='j-shop-info']/p[3]/span[@class='value']/text()''').extract()).strip()
            shopItem['shopUrl'] = 'https://mall.jd.com/index-'+shopId+'.html'
            shopItem['shopPhoneNumber'] = ''.join(response.xpath('''/html/body[@id='pop']/div[@class='forBack']/div[@id='wrap']/div[@class='j-rating-content']/div[@class='j-shop-info']/p[@class='phone']/text()''').extract()).strip()
            yield shopItem

            # 店家评价信息
            commentShopItem = ECommerceShopCommentItem()
            commentShopItem['eCommerceName'] = self.name
            commentShopItem['shopId'] = shopId
            commentShopItem['shopCommentsUrl'] = response.url
            commentData = dict()
            commentData['shopTotalRating'] = response.xpath('''/html/body[@id='pop']/div[@class='forBack']/div[@id='wrap']/div[@class='j-rating-content']/div[@class='j-rating-info']/div[@class='j-score total-score']/div/p[@class='total-score-num']/span/text()''').extract()[0]
            commentData['shopTotalRatingCTC'] = response.xpath('''/html/body[@id='pop']/div[@class='forBack']/div[@id='wrap']/div[@class='j-rating-content']/div[@class='j-rating-info']/div[@class='j-score total-score']/div/p[@class='score-des']/span[@class='percent']/text()''').extract()[0]
            commentShopItem['shopCommentsData']=str(commentData)
            yield commentShopItem