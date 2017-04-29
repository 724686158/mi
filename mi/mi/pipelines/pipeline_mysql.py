# -*- coding: utf-8 -*-
from twisted.enterprise import adbapi
import pymysql
from mi.items import ECommerce
from mi.items import ECommerceShopItem
from mi.items import ECommerceShopCommentItem
from mi.items import ECommerceGoodItem
from mi.items import ECommerceGoodCommentItem
class MysqlPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            db=settings['MYSQL_DBNAME'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor)
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        return cls(dbpool)


    def process_item(self, item, spider):
        if isinstance(item, ECommerce):
            query = self.dbpool.runInteraction(self._conditional_insert_ECommerce, item)  # 调用插入的方法
            query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法

        if isinstance(item, ECommerceShopItem):
            query = self.dbpool.runInteraction(self._conditional_insert_ECommerceShop, item)  # 调用插入的方法
            query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法

        if isinstance(item, ECommerceShopCommentItem):
            query = self.dbpool.runInteraction(self._conditional_insert_ECommerceShopComment, item)  # 调用插入的方法
            query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法

        if isinstance(item, ECommerceGoodItem):
            query = self.dbpool.runInteraction(self._conditional_insert_ECommerceGood, item)  # 调用插入的方法
            query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法

        if isinstance(item, ECommerceGoodCommentItem):
            query = self.dbpool.runInteraction(self._conditional_insert_ECommerceGoodComment, item)  # 调用插入的方法
            query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法

        return item

    # 向表ECommerce插入数据(共3字段)
    def _conditional_insert_ECommerce(self, tx, item):
        print "插入电商网站数据..."
        # 这个要根据item里的内容,以及表的结构来写
        sql = "insert into ECommerce(eCommerceId, eCommerceName, eCommerceUrl) values(%s,%s,%s)".encode(
            encoding='utf-8')
        params = (item["eCommerceId"], item["eCommerceName"], item["eCommerceUrl"])
        tx.execute(sql, params)
        try:

            print "插入电商网站数据成功"
        except:
            print "插入电商网站数据失败"

    # 向表ECommerceShop插入数据(共6字段)
    def _conditional_insert_ECommerceShop(self, tx, item):

        print "插入店家数据..."
        # 这个要根据item里的内容,以及表的结构来写
        sql = "insert into ECommerceShop(eCommerceId, shopId, shopName, shopUrl, shopLocation, shopPhoneNumber) values(%s,%s,%s,%s,%s,%s)".encode(
            encoding='utf-8')
        params = (item["eCommerceId"], item["shopId"], item["shopName"], item["shopUrl"], item["shopLocation"],
                  item["shopPhoneNumber"])
        tx.execute(sql, params)
        try:

            print "插入店家数据成功"
        except:
            print "插入店家数据失败"


    # 向表ECommerceShopComment插入数据(共4字段)
    def _conditional_insert_ECommerceShopComment(self, tx, item):

        print "插入店家评价数据..."
        # 这个要根据item里的内容,以及表的结构来写
        sql = "insert into ECommerceShopComment(eCommerceId, shopId, shopCommentsUrl, shopCommentsData) values(%s,%s,%s,%s)".encode(
            encoding='utf-8')
        params = (item["eCommerceId"], item["shopId"], item["shopCommentsUrl"], item["shopCommentsData"])
        tx.execute(sql, params)
        try:

            print "插入店家评价数据成功"
        except:
            print "插入店家评价数据失败"

    # 向表ECommerceGood插入数据(共6字段)
    def _conditional_insert_ECommerceGood(self, tx, item):
        print "插入商品数据..."
        # 这个要根据item里的内容,以及表的结构来写
        sql = "insert into ECommerceGood(eCommerceId, goodId, shopId, goodName, goodUrl, goodPrice) values(%s,%s,%s,%s,%s,%s)".encode(
            encoding='utf-8')
        params = (
            item["eCommerceId"], item["goodId"], item["shopId"], item["goodName"], item["goodUrl"], item["goodPrice"])
        tx.execute(sql, params)
        try:

            print "插入商品数据成功"
        except:
            print "插入商品数据失败"


    # 向表ECommerceGood插入数据(共4字段)
    def _conditional_insert_ECommerceGoodComment(self, tx, item):
        print "插入商品评价数据..."
        # 这个要根据item里的内容,以及表的结构来写
        sql = "insert into ECommerceGoodComment(eCommerceId, goodId, goodCommentsUrl, goodCommentsData) values(%s,%s,%s,%s)".encode(
            encoding='utf-8')
        params = (item["eCommerceId"], item["goodId"], item["goodCommentsUrl"], item["goodCommentsData"])
        tx.execute(sql, params)
        try:

            print "插入商品评价数据成功"
        except:
            print "插入商品评价数据失败"


    # 错误处理方法
    def _handle_error(self, failue, item, spider):
        print failue