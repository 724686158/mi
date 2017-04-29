# -*- coding: utf-8 -*-
from twisted.enterprise import adbapi
import pymysql
from items import ECommerce
from items import ECommerceShopItem
from items import ECommerceShopCommentItem
from items import ECommerceGoodItem
from items import ECommerceGoodCommentItem
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
        # 这个要根据item里的内容,以及表的结构来写
        sql = "insert into ECommerce(eCommerceId, eCommerceName, eCommerceUrl) values(%s,%s,%s)".encode(
            encoding='utf-8')
        params = (item["eCommerceId"], item["eCommerceName"], item["eCommerceUrl"])
        tx.execute(sql, params)

    # 向表ECommerceShop插入数据(共6字段)
    def _conditional_insert_ECommerceShop(self, tx, item):
        # 这个要根据item里的内容,以及表的结构来写
        sql = "insert into ECommerceShop(shopId, eCommerceId, shopName, shopUrl, shopLocation, shopPhoneNumber) values(%s,%s,%s,%s,%s,%s)".encode(encoding='utf-8')
        params = (item["shopId"], item["eCommerceId"], item["shopName"], item["shopUrl"], item["shopLocation"], item["shopPhoneNumber"])
        tx.execute(sql, params)

    # 向表ECommerceShopComment插入数据(共14字段)
    def _conditional_insert_ECommerceShopComment(self, tx, item):
        # 这个要根据item里的内容,以及表的结构来写
        sql = "insert into ECommerceShopComment(shopId, shopTotalRating, shopTotalRatingCTC, shopGoodQualitySatisficationRating, shopGoodQualitySatisficationRatingCTC, shopServiceSatisficationRating, shopServiceSatisficationRatingCTC, shopLogisticsSpeedSatisficationRating, shopLogisticsSpeedSatisficationRatingCTC, shopGoodDescriptionSatisficationRating, shopGoodDescriptionSatisficationRatingCTC, shopProcessingReturnAndExchangeGoodSatisficationRating, shopProcessingReturnAndExchangeGoodSatisficationRatingCTC, shopDisobeyRulesTimes) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".encode(encoding='utf-8')
        params = (item["shopId"], item["shopTotalRating"], item["shopTotalRatingCTC"], item["shopGoodQualitySatisficationRating"], item["shopGoodQualitySatisficationRatingCTC"], item["shopServiceSatisficationRating"], item["shopServiceSatisficationRatingCTC"], item["shopLogisticsSpeedSatisficationRating"], item["shopLogisticsSpeedSatisficationRatingCTC"], item["shopGoodDescriptionSatisficationRating"], item["shopGoodDescriptionSatisficationRatingCTC"], item["shopProcessingReturnAndExchangeGoodSatisficationRating"], item["shopProcessingReturnAndExchangeGoodSatisficationRatingCTC"], item["shopDisobeyRulesTimes"])
        tx.execute(sql, params)

    # 向表ECommerceGood插入数据(共5字段)
    def _conditional_insert_ECommerceGood(self, tx, item):
        # 这个要根据item里的内容,以及表的结构来写
        sql = "insert into ECommerceGood(goodId, shopId, goodName, goodUrl, goodPrice) values(%s,%s,%s,%s,%s)".encode(
            encoding='utf-8')
        params = (item["goodId"], item["shopId"], item["goodName"], item["goodUrl"], item["goodPrice"])
        tx.execute(sql, params)

    # 向表ECommerceGood插入数据(共8字段)
    def _conditional_insert_ECommerceGoodComment(self, tx, item):
        # 这个要根据item里的内容,以及表的结构来写
        sql = "insert into ECommerceGoodComment(goodId, goodCommentsCount, goodCommentsUrl, goodDisplayPictureCount, goodAddCommentCount, goodRankBetterCommentCount, goodRankMediateCommentCount, goodRankWorseCommentCount) values(%s,%s,%s,%s,%s,%s,%s,%s)".encode(
            encoding='utf-8')
        params = (item["goodId"], item["goodCommentsCount"], item["goodCommentsUrl"], item["goodDisplayPictureCount"], item["goodAddCommentCount"], item["goodRankBetterCommentCount"], item["goodRankMediateCommentCount"], item["goodRankWorseCommentCount"])
        tx.execute(sql, params)

    # 错误处理方法
    def _handle_error(self, failue, item, spider):
        print failue