# -*- coding: utf-8 -*-
import os
import json
import redis
import settings
from mysqlHelper import MysqlHelper
from mongoHelper import MongoHelper
from monitor_init import MonitorInit
from mysql_init import MysqlInit
from tld import get_tld
from gen_spiderInitfile_of_news import generate_spider_init

def get_redis(db_id):
    return redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, db_id)

def save_proxys(proxys):
    r = get_redis(settings.PROXY_DB)
    for proxy in proxys:
        r.lpush('valid_proxy',proxy)

def save_data(spider_name, json_str):
    r = get_redis(settings.SPIDERS_DB)
    js = dict(json.loads(json_str))
    r.set(spider_name, js)

# 获取新闻爬虫白名单
def get_whitelist():
    r = get_redis(settings.SPIDERS_DB)
    st = set()
    for i in r.keys():
        st.add(unicode(i, 'utf8'))
    return st

def split_target_urls(urls):
    # 用于分类爬虫(共三个类别： Whitelist, Fuzzy, Ecommerce)
    whitelist = []
    fuzzy = []
    ecommerce = []
    keys = get_whitelist()
    r = get_redis(settings.TASK_DB)
    # 获取新任务后清空数据库
    r.flushdb()
    oscwd = os.getcwd()
    for url in urls:
        spidername = get_tld(url, fail_silently=True)
        filename = oscwd + settings.TEMP_PATH + '/spiderInitfiles_of_eCommerce' + '/spiderInit_' + spidername + '.py'
        if os.path.isfile(filename):
            ecommerce.append(url)
            r.rpush('Ecommerce', url)
        elif spidername in keys:
            whitelist.append(url)
            r.rpush('Whitelist', url)
            generate_spider_init(spidername, {url})
        else:
            fuzzy.append(url)
            r.rpush('Fuzzy', url)
            generate_spider_init(spidername, {url})
    ans = {'Whitelist': whitelist, 'Fuzzy': fuzzy, 'Ecommerce': ecommerce}
    return ans

def classifier_urls(urls):
    oscwd = os.getcwd()
    r = get_redis(settings.CLASSIFIER_DB)
    keys = get_whitelist()
    for url in urls:
        spidername = get_tld(url, fail_silently=True)
        filename = oscwd + settings.TEMP_PATH + '/spiderInitfiles_of_eCommerce' + '/spiderInit_' + spidername + '.py'
        if os.path.isfile(filename):
            r.rpush('Ecommerce', url)
        elif spidername in keys:
            r.rpush('Whitelist', url)
            generate_spider_init(spidername, {url})
        else:
            r.rpush('Fuzzy', url)
            generate_spider_init(spidername, {url})

def get_spider_count_from_db():
    r = get_redis(settings.MONITOR_DB)
    keys = r.keys()
    arr = []
    for i in keys:
        if 'item_scraped_count_' in i:
            arr.append(i[i.rfind('_') + 1:])
    return arr

def init_monitor():
    # 初始化监控器数据
    monitor_init = MonitorInit()
    monitor_init.start()

def init_mysql():
    # 初始化mysql数据库
    mysql_init = MysqlInit()
    mysql_init.start()

def exec_init_of_missions():
    oscwd = os.getcwd()
    r = get_redis(settings.TASK_DB)
    news_spiders_need_fuzzymatching = r.lrange('0', 0, -1)
    news_spiders_in_whitelist = r.lrange('1', 0, -1)
    mission_urls = news_spiders_in_whitelist + news_spiders_need_fuzzymatching
    for mission_url in mission_urls:
        mission = get_tld(mission_url, fail_silently=True)
        filename =  oscwd + settings.TEMP_PATH + '/spiderInitfiles_of_news' + '/spiderInit_' + mission + '.py'
        if os.path.isfile(filename):
            print filename
            os.system('python2 ' + filename)
        else:
            print 'news_spider Init_' + mission + '.py' + ' not exist'

    ec_spiders = r.lrange('2', 0, -1)
    for mission_url in ec_spiders:
        mission = get_tld(mission_url, fail_silently=True)
        filename =  oscwd + settings.TEMP_PATH + '/spiderInitfiles_of_eCommerce' + '/spiderInit_' + mission + '.py'
        if os.path.isfile(filename):
            print filename
            os.system('python2 ' + filename)
        else:
            print 'eCommerce_spider Init_' + mission + '.py' + ' not exist'

def get_data_from_mongo(table_name):
    dic = []
    if(table_name == 'Article'):
        dic.append(('url', '标题', '正文', '关键词'))
        mongo = MongoHelper()
        db = mongo.connectDatabase()
        items = db['Article'].find()
        for item in items:
            t = (item['articleUrl'], item['articleTitle'], item['articleContent'], item['articleFirstTag'] + ' ' + item['articleSecondTag'] + ' ' + item['articleThirdTag'])
            dic.append(t)
    return dic

def get_data_from_mysql(table_name):
    dic = []
    if (table_name == 'ECommerce'):
        dic.append(('电商网站', '网站首页'))
        mysql = MysqlHelper()
        #sql = """SELECT * FROM %s LIMIT 0, 1000;""".encode(encoding='utf-8')
        sql = """SELECT * FROM ECommerce;""".encode(encoding='utf-8')
        results = mysql.select(sql)
        for col in results:
            t = (col['eCommerceName'], col['eCommerceUrl'])
            dic.append(t)
    if (table_name == 'ECommerceShop'):
        dic.append(('电商网站', '店铺ID', '店铺名称', '店铺链接', '店铺所在地', '店铺电话', '更新时间'))
        mysql = MysqlHelper()
        # sql = """SELECT * FROM %s LIMIT 0, 1000;""".encode(encoding='utf-8')
        sql = """SELECT * FROM ECommerceShop;""".encode(encoding='utf-8')
        results = mysql.select(sql)
        for col in results:
            t = (col['eCommerceName'], col['shopId'], col['shopName'], col['shopUrl'], col['shopLocation'], col['shopPhoneNumber'], col['updateTime'])
            dic.append(t)
    if (table_name == 'ECommerceShopComment'):
        dic.append(('电商网站', '店铺ID', '评论链接', '评论数据', '更新时间'))
        mysql = MysqlHelper()
        # sql = """SELECT * FROM %s LIMIT 0, 1000;""".encode(encoding='utf-8')
        sql = """SELECT * FROM ECommerceShopComment;""".encode(encoding='utf-8')
        results = mysql.select(sql)
        for col in results:
            t = (col['eCommerceName'], col['shopId'], col['shopCommentsUrl'], col['shopCommentsData'], col['updateTime'])
            dic.append(t)
    if (table_name == 'ECommerceGood'):
        dic.append(('电商网站', '商品ID', '店家ID', '商品名字', '商品链接', '商品价格', '更新时间'))
        mysql = MysqlHelper()
        # sql = """SELECT * FROM %s LIMIT 0, 1000;""".encode(encoding='utf-8')
        sql = """SELECT * FROM ECommerceGood;""".encode(encoding='utf-8')
        results = mysql.select(sql)
        for col in results:
            t = (col['eCommerceName'], col['goodId'], col['shopId'], col['goodName'], col['goodUrl'], col['goodPrice'], col['updateTime'])
            dic.append(t)
    if (table_name == 'ECommerceGoodComment'):
        dic.append(('电商网站', '商品ID', '评论链接', '评论数据', '更新时间'))
        mysql = MysqlHelper()
        # sql = """SELECT * FROM %s LIMIT 0, 1000;""".encode(encoding='utf-8')
        sql = """SELECT * FROM ECommerceGoodComment;""".encode(encoding='utf-8')
        results = mysql.select(sql)
        for col in results:
            t = (col['eCommerceName'], col['goodId'], col['goodCommentsUrl'], col['goodCommentsData'], col['updateTime'])
            dic.append(t)
    return dic

def batch_import_whitelist_of_news(txt):
    r = get_redis(settings.SPIDERS_DB)
    dic = eval(txt)
    for key in dic:
        r.set(key, dic[key])

def batch_export_whitelist_of_news():
    r = get_redis(settings.SPIDERS_DB)
    keys = r.keys()
    ans = {}
    for key in keys:
        ans[key] = r.get(key)
    return str(ans).encode('utf8')

def delete_news_in_whitelist(name):
    r = get_redis(settings.SPIDERS_DB)
    r.delete(name)

def clear_whitelist():
    r = get_redis(settings.SPIDERS_DB)
    r.flushdb()

def batch_import_proxys(txt):
    r = get_redis(settings.PROXY_DB)
    proxys = txt.split('\n')
    for proxy in proxys:
        if len(proxy) >= 2:
            print proxy
            r.sadd('valid_proxy', proxy)

def get_all_proxy():
    r = get_redis(settings.PROXY_DB)
    data = r.smembers('valid_proxy')
    return list(data)


def clear_proxys():
    r = get_redis(settings.PROXY_DB)
    r.flushdb()

def delte_proxy(proxy):
    r = get_redis(settings.PROXY_DB)
    print r.srem('valid_proxy', proxy)

def get_ecommerce_spider_name():
    names = []
    oscwd = os.getcwd()
    path = oscwd + settings.TEMP_PATH + '/spiderInitfiles_of_eCommerce'
    files = os.listdir(path)
    for file in files:
        if 'spiderInit_' in file:
            spidername = file.replace('spiderInit_', '').replace('.py', '')
            names.append(spidername)
    return names

def get_news_spider_name():
    r = get_redis(settings.SPIDERS_DB)
    keys = r.keys()
    print type(keys)
    return keys

def get_news_spider_describe(name):
    r = get_redis(settings.SPIDERS_DB)
    attr = r.get(name)
    describe = eval(attr)['name']
    return describe

def delte_filter_db():
    r = get_redis(settings.FILTER_DB)
    r.flushdb()

def add_resources_redis(name, info_dic):
    r = get_redis(settings.RESOURCES_REDIS_DB)
    r.set(name, str(info_dic))

def add_resources_mysql(name, info_dic):
    r = get_redis(settings.RESOURCES_MYSQL_DB)
    r.set(name, str(info_dic))

def add_resources_mongo(name, info_dic):
    r = get_redis(settings.RESOURCES_MONGO_DB)
    r.set(name, str(info_dic))

def get_resources_redis():
    r = get_redis(settings.RESOURCES_REDIS_DB)
    keys = r.keys()
    data = []
    for key in keys:
        dic = {}
        dic['name'] = key
        dic['type'] = 'Redis'
        dic['detail'] = eval(r.get(key))
        data.append(dic)
    return data

def get_resources_mysql():
    r = get_redis(settings.RESOURCES_MYSQL_DB)
    keys = r.keys()
    data = []
    for key in keys:
        dic = {}
        dic['name'] = key
        dic['type'] = 'Mysql'
        dic['detail'] = eval(r.get(key))
        data.append(dic)
    return data

def get_resources_mongo():
    r = get_redis(settings.RESOURCES_MONGO_DB)
    keys = r.keys()
    data = []
    for key in keys:
        dic = {}
        dic['name'] = key
        dic['type'] = 'Mongo'
        dic['detail'] = eval(r.get(key))
        data.append(dic)
    return data

def delete_resources(name, type):
    if type == 'Redis':
        r = get_redis(settings.RESOURCES_REDIS_DB)
        r.delete(name)
    elif type == 'Mysql':
        r = get_redis(settings.RESOURCES_MYSQL_DB)
        r.delete(name)
    elif type == 'Mongo':
        r = get_redis(settings.RESOURCES_MONGO_DB)
        r.delete(name)

def add_settings(name, info_dic):
    r = get_redis(settings.SETTINGS_DB)
    r.set(name, str(info_dic))

def delete_settings(name):
    r = get_redis(settings.SETTINGS_DB)
    r.delete(name)

def get_settings():
    r = get_redis(settings.SETTINGS_DB)
    keys = r.keys()
    data = []
    for key in keys:
        dic = {}
        dic['name'] = key
        dic['detail'] = eval(r.get(key))
        data.append(dic)
    return data

def get_settings_name():
    r = get_redis(settings.SETTINGS_DB)
    keys = r.keys()
    return keys

#

def add_submission(name, info_dic):
    r = get_redis(settings.SUBMISSION_DB)
    r.set(name, str(info_dic))

def get_all_submission():
    r = get_redis(settings.SUBMISSION_DB)
    keys = r.keys()
    data = []
    for key in keys:
        dic = {}
        dic['name'] = key
        dic['detail'] = eval(r.get(key))
        data.append(dic)
    return data

# 根据名字获取一个子任务的信息, 返回字典格式
def get_submission(name):
    r = get_redis(settings.SUBMISSION_DB)
    return {name: r.get(get_redis)}

def get_all_submission_name():
    r = get_redis(settings.SUBMISSION_DB)
    keys = r.keys()
    return keys

def delete_submission(name):
    r = get_redis(settings.SUBMISSION_DB)
    r.delete(name)


def add_mission(name, info_dic):
    r = get_redis(settings.MISSION_DB)
    r.set(name, str(info_dic))

def get_all_mission():
    r = get_redis(settings.MISSION_DB)
    keys = r.keys()
    data = []
    for key in keys:
        dic = {}
        dic['name'] = key
        dic['detail'] = eval(r.get(key))
        data.append(dic)
    return data

# 根据名字获取一个子任务的信息, 返回字典格式
def get_mission(name):
    r = get_redis(settings.MISSION_DB)
    return {name: r.get(get_redis)}

def get_all_mission_name():
    r = get_redis(settings.MISSION_DB)
    keys = r.keys()
    return keys

def delete_mission(name):
    r = get_redis(settings.MISSION_DB)
    r.delete(name)

