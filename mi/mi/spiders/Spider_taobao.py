#  -*- coding: utf-8 -*-

import redis
import mi.settings as prime_settings

import scrapy
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from mi.items import ECommerceGoodItem
from mi.items import ECommerceGoodCommentItem
from mi.items import ECommerceShopCommentItem
from mi.items import ECommerceShopItem
import re
import json
import urllib



class Spider_taobao(RedisCrawlSpider):
    redis_key = 'taobao:start_urls'
    name = 'taobao'
    allowed_domains = ['taobao.com']
    # 电商Id
    eCommerceId = 4

    queryUrlSegment1 = 'https://s.taobao.com/api?_ksTS=1488096888907_219&ajax=true&m=customized&rn=4f751d9d86dcf1ac3d0f81b6aa8ec720&q='
    queryUrlSegment2 = '&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20170507&ie=utf8&s='
    queryUrlSegment3 = '&bcoffset=-3'

    itemUrlSegment1 = 'https://item.taobao.com/item.htm?spm=a230r.1.14.59.9StjRh&id='
    itemUrlSegment2 = '&ns=1&abbucket=17#detail'

    rules = {

        Rule(LinkExtractor(allow=('.*//s.taobao.com/search.*')), callback='processSearchPage', follow=True),
        Rule(LinkExtractor(allow=('.*'), deny=('.*act.*', '.*service.*', '.*support.*', '.*partner.*', '.*gongyi.*', '.*login.*', '.*wangxin.*')), follow=True)
    }


    def start_requests(self):
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, prime_settings.RUNNINGDATA_DB)
        keywords = r.lrange("taobao:item_types", 0, -1)
        for key in keywords:
            yield scrapy.Request(url='https://s.taobao.com/search?q=' + str(
                key) + '&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170506'
                                 , callback=self.processSearchPage, meta={'key': str(key)})


    def processSearchPage(self, response):
        try:
            key = response.meta['key']
        except:
            pattern = re.compile(r'q=[\u4e00-\u9fa5]+')
            pattern2 = re.compile(r'[\u4e00-\u9fa5]+')
            key = str(pattern.findall(urllib.parse.unquote(response.url)))
            key = pattern2.findall(key)[0]

        yield scrapy.Request(url=self.queryUrlSegment1 + str(key) + self.queryUrlSegment2 + '0' + self.queryUrlSegment3,
                             meta={'key': str(key), 'count': 0}, callback=self.processEcommerceGoodAndShopInformation,
                             )

    def processEcommerceGoodAndShopInformation(self, response):
        html = json.loads(response.body.replace('}}});', '}}}'))
        if html['API.CustomizedApi']['itemlist']['auctions'] is None:
            return

        for eve in html['API.CustomizedApi']['itemlist']['auctions']:
            tempGoodItem = ECommerceGoodItem()
            tempGoodItem['eCommerceId'] = self.eCommerceId
            # 商品的数据
            tempGoodItem['goodName'] = eve['raw_title']
            tempGoodItem['goodId'] = eve['nid']
            tempGoodItem['shopId'] = eve['user_id']
            tempGoodItem['goodPrice'] = eve['view_price']
            tempGoodItem['goodUrl'] = self.itemUrlSegment1 + tempGoodItem['goodId'] + self.itemUrlSegment2
            yield tempGoodItem
            # 商品的评论数据
            tempGoodCommentItem = ECommerceGoodCommentItem()
            tempGoodCommentItem['eCommerceId'] = self.eCommerceId
            tempGoodCommentItem['goodId'] = eve['nid']
            tempGoodCommentItem['goodCommentsUrl'] = 'https:' + eve['comment_url']
            goodData = {
                'saleCount': eve['view_sales'],
                'commentCount': eve['comment_count']
            }
            tempGoodCommentItem['goodCommentsData'] = str(goodData)
            yield tempGoodCommentItem


            # 店铺数据
            tempShopItem = ECommerceShopItem()
            tempShopItem['eCommerceId'] = self.eCommerceId
            tempShopItem['shopId'] = eve['user_id']
            tempShopItem['shopName'] = eve['nick']
            tempShopItem['shopLocation'] = eve['item_loc']
            tempShopItem['shopUrl'] = ''
            tempShopItem['shopPhoneNumber'] = ''
            yield scrapy.Request(url=tempGoodItem['goodUrl'], callback=self.processGoodPage,
                                 meta={'shopItem': tempShopItem})

            # 店铺评论数据
            tempShopCommentItem = ECommerceShopCommentItem()
            tempShopCommentItem['eCommerceId'] = self.eCommerceId
            tempShopCommentItem['shopId'] = eve['user_id']
            tempShopCommentItem['shopCommentsUrl'] = ''
            shopCommentData = {
                'isTmall': eve['shopcard']['isTmall'],
                'shopCredit': eve['shopcard']['sellerCredit'],
                'shopTotalRate': eve['shopcard']['totalRate']
            }
            tempShopCommentItem['shopCommentsData'] = str(shopCommentData)
            yield tempShopCommentItem

            try:
                yield scrapy.Request(
                url=self.queryUrlSegment1 + str(response.meta['key']) + self.queryUrlSegment2 + str(
                    int(response.meta['count']) + 13) + self.queryUrlSegment3,
                meta={'key': str(response.meta['key']), 'count': int(response.meta['count']) + 13},
                callback=self.processEcommerceGoodAndShopInformation)
            except:
                print ('nextPageFailed')

    def processGoodPage(self, response):
        tempShopItem = response.meta['shopItem']

        pattern = re.compile(r'shopId:"\d+"')
        pattern2 = re.compile(r'\d+')
        try:
            shopId = pattern2.findall(str(pattern.findall(str(response.body))))[0]
            tempShopItem['shopUrl'] = 'https://shop' + str(shopId) + '.taobao.com/'
        except:
            tempShopItem['shopUrl']=''
            yield tempShopItem


