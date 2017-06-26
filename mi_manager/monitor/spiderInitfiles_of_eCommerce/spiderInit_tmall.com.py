# -*- coding: utf-8 -*-
import requests
from lxml import html

import redis

import monitor.settings as prime_settings
from monitor.mysqlHelper import MysqlHelper


def init():

    print "try insert eCommerceId......"
    try:
        db = MysqlHelper()
        sql = "insert into ECommerce(eCommerceName, eCommerceUrl) values('taobao.com', 'https://www.taobao.com');".encode(encoding='utf-8')
        db.insert(sql)
        print "insert eCommerceId success"
    except Exception:
        print "insert eCommerceId failed"


    print "pushing taobao_start_url......"
    try:
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db=prime_settings.FILTER_DB)
        r.delete("taobao:start_urls")
        r.delete("taobao:dupefilter" + "0")
        r.delete("taobao:requests")
        r.lpush("taobao:start_urls", 'https://www.taobao.com')
        print "pushing taobao_start_url success"
    except Exception:
        print "pushing taobao_start_url failed"

    try:
        print "尝试获取淘宝商品种类..."
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, prime_settings.RUNNINGDATA_DB)
        r.delete("taobao:item_types")
        keywords = []
        response = requests.get(
            url='https://www.taobao.com/tbhome/page/market-list?spm=a21bo.50862.201867-main.1.Xec2Ce')
        tree = html.fromstring(response.text)
        themes = tree.xpath('//a[@class="category-name category-name-level1 J_category_hash"]')
        for theme in themes:
            themeWord = ''.join(theme.xpath('./text()'))
            keywords.append(themeWord)
        categoryNames = tree.xpath('//a[@class="category-name"]')
        for categoryName in categoryNames:
            categoryNameWord = ''.join(categoryName.xpath('./text()'))
            keywords.append(categoryNameWord)
        for key in keywords:
            r.lpush("taobao:item_types", key)
        print "获取淘宝商品种类成功"
    except Exception:
        print "获取淘宝商品种类失败"

    try:
        print "尝试加入cookie用户帐号信息..."
        r = redis.Redis(prime_settings.REDIS_HOST, prime_settings.REDIS_PORT, db = prime_settings.COOKIES_DB)
        r.lpush("taobao", 'omtbreak')
        print "尝试加入cookie用户帐号信息成功"
    except Exception:
        print "尝试加入cookie用户帐号信息失败"

if __name__ == '__main__':
    init()
