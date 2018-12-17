# -*- coding: utf-8 -*-
from twisted.enterprise import adbapi
import pymysql
from mi.items import ECommerceItem
from mi.items import ECommerceShopItem
from mi.items import ECommerceShopCommentItem
from mi.items import ECommerceGoodItem
from mi.items import ECommerceGoodCommentItem


class MysqlPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        try:
            dbparams = dict(
                host=settings['MYSQL_HOST'],
                user=settings['MYSQL_USER'],
                passwd=settings['MYSQL_PASSWD'],
                db=settings['MYSQL_DBNAME'],
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor)
            dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
            return cls(dbpool)
        except:
            print '获取配置信息出错'

    def process_item(self, item, spider):
        if isinstance(item, ECommerceItem):
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
        # 这个要根据item里的内容,以及表的结构来写
        try:
            sql = "insert into ECommerce(eCommerceName, eCommerceUrl) values(%s,%s)".encode(
                encoding='utf-8')
            params = (item["eCommerceName"], item["eCommerceUrl"])
            tx.execute(sql, params)
            print "插入电商网站数据成功"
        except Exception as e:
            print "插入电商网站数据失败" + e.message

    # 向表ECommerceShop插入数据(共6字段)
    def _conditional_insert_ECommerceShop(self, tx, item):
        # 这个要根据item里的内容,以及表的结构来写
        try:
            sql = "insert into ECommerceShop(eCommerceName, shopId, shopName, shopUrl, shopLocation, shopPhoneNumber) values(%s,%s,%s,%s,%s,%s)".encode(
                encoding='utf-8')
            params = (item["eCommerceName"], item["shopId"], item["shopName"], item["shopUrl"], item["shopLocation"],
                      item["shopPhoneNumber"])
            tx.execute(sql, params)
            print "插入店家数据成功"
        except Exception as e:
            print "插入店家数据失败" + e.message


    # 向表ECommerceShopComment插入数据(共4字段)
    def _conditional_insert_ECommerceShopComment(self, tx, item):
        # 这个要根据item里的内容,以及表的结构来写
        try:
            sql = "insert into ECommerceShopComment(eCommerceName, shopId, shopCommentsUrl, shopCommentsData) values(%s,%s,%s,%s)".encode(
                encoding='utf-8')
            params = (item["eCommerceName"], item["shopId"], item["shopCommentsUrl"], item["shopCommentsData"])
            tx.execute(sql, params)
            print "插入店家评价数据成功"
        except Exception as e:
            print "插入店家评价数据失败" + e.message

    # 向表ECommerceGood插入数据(共6字段)
    def _conditional_insert_ECommerceGood(self, tx, item):
        # 这个要根据item里的内容,以及表的结构来写
        try:
            sql = "insert into ECommerceGood(eCommerceName, goodId, shopId, goodName, goodUrl, goodPrice) values(%s,%s,%s,%s,%s,%s)".encode(
                encoding='utf-8')
            params = (
                item["eCommerceName"], item["goodId"], item["shopId"], item["goodName"], item["goodUrl"],
                item["goodPrice"])
            tx.execute(sql, params)
            print "插入商品数据成功"
        except Exception as e:
            print "插入商品数据失败" + e.message

    # 向表ECommerceGood插入数据(共4字段)
    def _conditional_insert_ECommerceGoodComment(self, tx, item):
        # 这个要根据item里的内容,以及表的结构来写
        try:
            sql = "insert into ECommerceGoodComment(eCommerceName, goodId, goodCommentsUrl, goodCommentsData) values(%s,%s,%s,%s)".encode(
                encoding='utf-8')
            params = (item["eCommerceName"], item["goodId"], item["goodCommentsUrl"], item["goodCommentsData"])
            tx.execute(sql, params)
            print "插入商品评价数据成功"
        except Exception as e:
            print "插入商品评价数据失败" + e.message

    # 错误处理方法
    def _handle_error(self, failue, item, spider):
        print failue