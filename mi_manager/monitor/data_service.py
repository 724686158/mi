# -*- coding: utf-8 -*-
import os
import json
import redis
import settings
import time
from mysqlHelper import MysqlHelper
from mongoHelper import MongoHelper
from monitor_init import MonitorInit
from mysql_init import MysqlInit
from tld import get_tld
from gooseHelper import GooseHelper

Time = lambda: time.strftime('%Y-%m-%d %H:%M:%S')

########################################################################################################################
# 特殊操作

# 连接redis数据库
def get_redis(db_id):
    return redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, db_id)

# 获取电商爬虫名称列表
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

# 获取受监控器监控的爬虫的列表
def get_spider_count_from_db():
    r = get_redis(settings.MONITOR_DB)
    keys = r.keys()
    arr = []
    for i in keys:
        if 'item_scraped_count_' in i:
            arr.append(i[i.rfind('_') + 1:])
    return arr

# 初始化监控器数据
def init_monitor():
    monitor_init = MonitorInit()
    monitor_init.start()

# 初始化mysql数据库
def init_mysql(name = settings.MYSQL_DBNAME):
    mysql_init = MysqlInit()
    mysql_init.start(name)

# 清理去重队列
def delte_filter_db():
    r = get_redis(settings.FILTER_DB)
    r.flushdb()

# 运行初始化文件
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
            os.system('python ' + filename)
        else:
            print 'news_spider Init_' + mission + '.py' + ' not exist'
    ec_spiders = r.lrange('2', 0, -1)
    for mission_url in ec_spiders:
        mission = get_tld(mission_url, fail_silently=True)
        filename =  oscwd + settings.TEMP_PATH + '/spiderInitfiles_of_eCommerce' + '/spiderInit_' + mission + '.py'
        if os.path.isfile(filename):
            os.system('python ' + filename)
        else:
            print 'eCommerce_spider Init_' + mission + '.py' + ' not exist'

# 从mongo数据库获取数据
def get_data_from_mongo(table_name, mission_name = settings.MONGO_DATABASE):
    dic = []
    if(table_name == 'Article'):
        dic.append(('url', '标题', '正文', '关键词'))
        mongo = MongoHelper()
        db = mongo.discovery_and_connectDatabase_for_mission(mission_name)
        #db = mongo.connectDatabase(mission_name)
        items = db['Article'].find()
        for item in items:
            t = (item['articleUrl'], item['articleTitle'], item['articleContent'], item['articleFirstTag'] + ' ' + item['articleSecondTag'] + ' ' + item['articleThirdTag'])
            dic.append(t)
    return dic

# 从mysql数据库获取数据
def get_data_from_mysql(table_name, mission_name = settings.MYSQL_DBNAME):
    dic = []
    if (table_name == 'ECommerce'):
        dic.append(('电商网站', '网站首页'))
        mysql = MysqlHelper()
        #sql = """SELECT * FROM %s LIMIT 0, 1000;""".encode(encoding='utf-8')
        sql = """SELECT * FROM ECommerce;""".encode(encoding='utf-8')
        results = mysql.select_for_mission(mission_name, sql)
        for col in results:
            t = (col['eCommerceName'], col['eCommerceUrl'])
            dic.append(t)
    if (table_name == 'ECommerceShop'):
        dic.append(('电商网站', '店铺ID', '店铺名称', '店铺链接', '店铺所在地', '店铺电话', '更新时间'))
        mysql = MysqlHelper()
        # sql = """SELECT * FROM %s LIMIT 0, 1000;""".encode(encoding='utf-8')
        sql = """SELECT * FROM ECommerceShop;""".encode(encoding='utf-8')
        results = mysql.select_for_mission(mission_name, sql)
        for col in results:
            t = (col['eCommerceName'], col['shopId'], col['shopName'], col['shopUrl'], col['shopLocation'], col['shopPhoneNumber'], col['updateTime'])
            dic.append(t)
    if (table_name == 'ECommerceShopComment'):
        dic.append(('电商网站', '店铺ID', '评论链接', '评论数据', '更新时间'))
        mysql = MysqlHelper()
        # sql = """SELECT * FROM %s LIMIT 0, 1000;""".encode(encoding='utf-8')
        sql = """SELECT * FROM ECommerceShopComment;""".encode(encoding='utf-8')
        results = mysql.select_for_mission(mission_name, sql)
        for col in results:
            t = (col['eCommerceName'], col['shopId'], col['shopCommentsUrl'], col['shopCommentsData'], col['updateTime'])
            dic.append(t)
    if (table_name == 'ECommerceGood'):
        dic.append(('电商网站', '商品ID', '店家ID', '商品名字', '商品链接', '商品价格', '更新时间'))
        mysql = MysqlHelper()
        # sql = """SELECT * FROM %s LIMIT 0, 1000;""".encode(encoding='utf-8')
        sql = """SELECT * FROM ECommerceGood;""".encode(encoding='utf-8')
        results = mysql.select_for_mission(mission_name, sql)
        for col in results:
            t = (col['eCommerceName'], col['goodId'], col['shopId'], col['goodName'], col['goodUrl'], col['goodPrice'], col['updateTime'])
            dic.append(t)
    if (table_name == 'ECommerceGoodComment'):
        dic.append(('电商网站', '商品ID', '评论链接', '评论数据', '更新时间'))
        mysql = MysqlHelper()
        # sql = """SELECT * FROM %s LIMIT 0, 1000;""".encode(encoding='utf-8')
        sql = """SELECT * FROM ECommerceGoodComment;""".encode(encoding='utf-8')
        results = mysql.select_for_mission(mission_name, sql)
        for col in results:
            t = (col['eCommerceName'], col['goodId'], col['goodCommentsUrl'], col['goodCommentsData'], col['updateTime'])
            dic.append(t)
    return dic

def get_data_from_goose(urls):
    gooseHelp = GooseHelper()
    return gooseHelp.get_news_of_urls(urls)


# 获取需要用户注意的模糊爬虫的名单
def get_fuzzy_list():
    r = get_redis(settings.CLASSIFIER_DB)
    return r.lrange('Fuzzy', 0, -1)

# 对URL进行分类 并返回三个爬虫名单列表(Ecommerce, Whitelist, Fuzzy)
def classifier_urls(urls):
    oscwd = os.getcwd()
    r = get_redis(settings.CLASSIFIER_DB)
    keys = get_whitelist()
    ecommerce_spiders = []
    whitelist_spiders = []
    fuzzy_spiders = []
    for url in urls:
        spidername = get_tld(url, fail_silently=True)
        if spidername:
            filename = oscwd + settings.TEMP_PATH + '/spiderInitfiles_of_eCommerce' + '/spiderInit_' + spidername + '.py'
            if os.path.isfile(filename):
                r.rpush('Ecommerce', url)
                ecommerce_spiders.append(url)
            elif spidername in keys:
                r.rpush('Whitelist', url)
                whitelist_spiders.append(url)
            else:
                r.rpush('Fuzzy', url)
                fuzzy_spiders.append(url)
    return ecommerce_spiders, whitelist_spiders, fuzzy_spiders

# 旧API, 分类URL (弃用)
def split_target_urls(urls):
    # 用于分类爬虫(共三个类别： Whitelist, Fuzzy, Ecommerce)
    whitelist = []
    fuzzy = []
    ecommerce = []
    keys = get_whitelist()
    r = get_redis(settings.CLASSIFIER_DB)
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
        else:
            fuzzy.append(url)
            r.rpush('Fuzzy', url)
    ans = {'Whitelist': whitelist, 'Fuzzy': fuzzy, 'Ecommerce': ecommerce}
    return ans

# 将url作为爬虫任务的start_url(存在问题, 未使用)
def push_urls_as_start_url(urls):
    r = get_redis(settings.FILTER_DB)
    for url in urls:
        spidername = get_tld(url, fail_silently=True)
        r.lpush(spidername + ':start_urls', url)

# 获取MESOS控制台的URL
def get_mesos_url():
    r = get_redis(settings.SYMBOL_DB)
    return  r.get('mesos_url')

# 获取MARATHON控制台的URL
def get_marathon_url():
    r = get_redis(settings.SYMBOL_DB)
    return  r.get('marathon_url')

# 获取系统内时间
def get_now_time():
    return Time

# 获取任务权重饼状图
def get_piechart_of_mission():
    # 获取全部任务的信息
    data = []
    r = get_redis(settings.MISSION_DB)
    keys = r.keys()
    for key in keys:
        detail = eval(r.get(key))
        if detail['state'] != 'STOP':
            data.append({'value': float(detail['weight']), 'name': key})
    return data

# 获取调度队列中最优先N个task
def get_top_task(number):
    ans = []
    ans.append(('顺位', '任务名', '爬虫任务'))
    r = get_redis(settings.DISPATCH_DB)
    tasks = r.zrange('task_zset', 0, number, desc = True)
    dix = 1
    for task in tasks:
        detail = eval(task)
        ans.append((str(dix), detail['father_mission_name'],detail['spider_name']))
        dix = dix + 1
    while dix <= 10:
        ans.append((str(dix), '', ''))
        dix = dix + 1
    return ans

def get_top_submissions():
    ans = []
    ans.append(('实际优先度', '任务名', '爬虫任务'))
    r = get_redis(settings.DISPATCH_DB)
    tasks = r.zrange('submission_zset', 0, -1, desc = True, withscores=True)
    for task in tasks:
        detail = eval(task[0])
        ans.append((str(task[1]), detail['father_mission_name'], detail['spider_name']))
    return ans

def login_system(username, password):
    r = get_redis(settings.SYMBOL_DB)
    if r.get(username) == password:
        if r.get('now_login_time'):
            r.set('lost_login_time', r.get('now_login_time'))
            r.set('now_login_time', Time())
        else:
            r.set('now_login_time', Time())
        return 'True'
    else:
        return 'False'

def get_last_login_time():
    r = get_redis(settings.SYMBOL_DB)
    if r.get('lost_login_time'):
        return '上一次登录系统的时间是为[' + r.get('lost_login_time') + ']'
    else:
        return '首次登录, 点击页面右上角可查看使用帮助'

########################################################################################################################

########################################################################################################################
# ECommerce

# 获取电商爬虫名称列表
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

def get_number_of_ecommerce():
    return  len(get_ecommerce_spider_name())



########################################################################################################################

########################################################################################################################
# WHITELIST
def get_number_of_whitelist():
    r = get_redis(settings.SPIDERS_DB)
    keys = r.keys()
    return len(keys)
# 获取白名单中爬虫名称清单
def get_news_spider_name():
    r = get_redis(settings.SPIDERS_DB)
    keys = r.keys()
    return keys

# 根据名称从白名单数据库中提取对应爬虫的描述
def get_news_spider_describe(name):
    r = get_redis(settings.SPIDERS_DB)
    attr = r.get(name)
    describe = eval(attr)['name'] # 兼容数据接口的变化, 此处的name字段义为describe
    return describe

# 保存新闻爬虫信息到白名单
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

# 批量导出白名单
def batch_import_whitelist_of_news(txt):
    r = get_redis(settings.SPIDERS_DB)
    dic = eval(txt)
    for key in dic:
        r.set(key, dic[key])

# 批量导入白名单
def batch_export_whitelist_of_news():
    r = get_redis(settings.SPIDERS_DB)
    keys = r.keys()
    ans = {}
    for key in keys:
        ans[key] = r.get(key)
    return str(ans).encode('utf8')

# 根据名字删除白名单中的一个新闻爬虫
def delete_news_in_whitelist(name):
    r = get_redis(settings.SPIDERS_DB)
    r.delete(name)

# 清空新闻爬虫白名单
def clear_whitelist():
    r = get_redis(settings.SPIDERS_DB)
    r.flushdb()

########################################################################################################################

########################################################################################################################
# PROXY
def save_proxys(proxys):
    r = get_redis(settings.PROXY_DB)
    for proxy in proxys:
        r.lpush('valid_proxy',proxy)

def batch_import_proxys(txt):
    r = get_redis(settings.PROXY_DB)
    proxys = txt.split('\n')
    for proxy in proxys:
        if len(proxy) >= 2:
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
########################################################################################################################

########################################################################################################################
# RESOURCES
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
def get_all_redis_resources_name():
    r = get_redis(settings.RESOURCES_REDIS_DB)
    return r.keys()

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

def get_all_mysql_resources_name():
    r = get_redis(settings.RESOURCES_MYSQL_DB)
    return r.keys()

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

def get_all_mongo_resources_name():
    r = get_redis(settings.RESOURCES_MONGO_DB)
    return r.keys()

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
########################################################################################################################

########################################################################################################################
# SETTINGS
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
########################################################################################################################

########################################################################################################################
# SUBMISSION
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

# 根据任务名称和爬虫类型生成默认子任务
def get_default_submissions(mission_name, url, type):
    spider = get_tld(url, fail_silently=True)
    name = str(mission_name + '_' + spider)
    spider_name = str(spider)
    if type == 'Ecommerce':
        settings = '电商类爬虫默认配置'
    elif type == 'Whitelist':
        settings = '新闻类爬虫默认配置'
    elif type == 'Fuzzy':
        settings = '新闻类爬虫默认配置'
    else:
        settings = '默认设置'
    priority = 1
    return {"name": name, "detail": {"spider_name": spider_name, "settings": settings, "priority": priority, "start_url": url, "type": type}}

########################################################################################################################

########################################################################################################################
# MISSION
# 根据爬虫名和任务名, 生成默认的子任务
def add_mission(name, info_dic):
    r = get_redis(settings.MISSION_DB)
    r.set(name, str(info_dic))
    init_mysql(name)
    missions_change()

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

# 根据名字获取任务的信息, 返回字典格式
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
    missions_change()

def mission_start(name):
    r = get_redis(settings.MISSION_DB)
    detail = r.get(name)
    # 首先更新任务状态
    new_detail = eval(detail)
    new_detail['state'] = 'START'
    r.set(name, str(new_detail))
    missions_change()

def mission_stop(name):
    r = get_redis(settings.MISSION_DB)
    detail = r.get(name)
    # 首先更新任务状态
    new_detail = eval(detail)
    new_detail['state'] = 'STOP'
    r.set(name, str(new_detail))
    missions_change()

# 在数据库中设置信号量, 标记任务发生了改变
def missions_change():
    r = get_redis(settings.SYMBOL_DB)
    r.set('MISSIONS_CHANGE', '1')

########################################################################################################################
