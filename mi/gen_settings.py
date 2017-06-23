# -*- coding: utf-8 -*-
import os
import settings

# mi模块setting.py的模板
setting_template_of_mi = '''\
# -*- coding: utf-8 -*-
BOT_NAME = '%s'
SUB_MISSION = '%s'
ROBOTSTXT_OBEY = %s
COOKIES_ENABLED = %s
RETRY_ENABLED = %s
HTTP_PROXY_ENABLED = %s
AUTOTHROTTLE_ENABLED = %s
AUTOTHROTTLE_START_DELAY = %s
AUTOTHROTTLE_MAX_DELAY = %s
DOWNLOAD_DELAY = %s
CONCURRENT_REQUESTS_PER_DOMAIN = %s
DOWNLOAD_TIMEOUT = %s
REDIS_HOST = '%s'
REDIS_PORT = %s
FILTER_HOST = '%s'
FILTER_PORT = %s
MYSQL_HOST = '%s'
MYSQL_PORT = %s
MYSQL_DBNAME = '%s'
MYSQL_USER = '%s'
MYSQL_PASSWD = '%s'
MONGO_HOST = '%s'
MONGO_PORT = %s
MONGO_DATABASE = '%s'
COOKIES_DEBUG = True
AUTOTHROTTLE_DEBUG = True
SPIDER_MODULES = ['mi.spiders_of_eCommerce', 'mi.spiders_of_news_in_whiteList', 'mi.spiders_of_news_need_fuzzymatching']
##############################################################################################
FILTER_DB = 0
SYMBOL_DB = 1
TASK_DB = 2
DISPATCH_DB = 3
MISSION_DB = 4
SUBMISSION_DB = 5
SETTINGS_DB = 6
RESOURCES_REDIS_DB = 7
RESOURCES_MYSQL_DB = 8
RESOURCES_MONGO_DB = 9
PROXY_DB = 10
RUNNINGDATA_DB = 11
COOKIES_DB = 12
SPIDERS_DB = 13
CLASSIFIER_DB = 14
MONITOR_DB = 15
##############################################################################################
STATS_KEYS = ["downloader/request_count", "downloader/response_count", "downloader/response_status_count/200", "item_scraped_count"]
ITEM_PIPELINES = {
    'mi.pipelines.pipeline_mongo.MongoPipeline':300,
    'mi.pipelines.pipeline_mysql.MysqlPipeline':301,
}
DOWNLOADER_MIDDLEWARES = {
    'mi.middlewares.middleware_proxy.RandomProxyMiddleware':HTTP_PROXY_ENABLED,
    'mi.middlewares.middleware_rotateUserAgent.RotateUserAgentMiddleware': 401,
    'mi.middlewares.middleware_monitor.StatcollectorMiddleware': 402,
    'mi.middlewares.middleware_cookie.CookieMiddleware': None,
}
RETRY_TIMES = 6
PROXY_USED_TIMES = 2
RETRY_HTTP_CODES = [500, 503, 504, 599, 403]
SCHEDULER = 'mi.scrapy_redis.scheduler.Scheduler'
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'mi.scrapy_redis.queue.SpiderPriorityQueue'
DOWNLOAD_HANDLERS = {'s3': None,}\
'''

def generate_setting_of_mi(task):
    print task
    dic = eval(task)
    father_mission_name = dic['father_mission_name']
    spider_name = dic['spider_name']
    settings_detail = dic['settings_detail']
    settings_detail_dic = eval(settings_detail)
    ROBOTSTXT_OBEY = settings_detail_dic['ROBOTSTXT_OBEY']
    COOKIES_ENABLED = settings_detail_dic['COOKIES_ENABLED']
    RETRY_ENABLED = settings_detail_dic['RETRY_ENABLED']
    if settings_detail_dic['HTTP_PROXY_ENABLED'] == 'True':
        HTTP_PROXY_ENABLED = '400'
    else:
        HTTP_PROXY_ENABLED = 'None'
    AUTOTHROTTLE_ENABLED = settings_detail_dic['AUTOTHROTTLE_ENABLED']
    AUTOTHROTTLE_START_DELAY = settings_detail_dic['AUTOTHROTTLE_START_DELAY']
    AUTOTHROTTLE_MAX_DELAY = settings_detail_dic['AUTOTHROTTLE_MAX_DELAY']
    DOWNLOAD_DELAY = settings_detail_dic['DOWNLOAD_DELAY']
    CONCURRENT_REQUESTS_PER_DOMAIN = settings_detail_dic['CONCURRENT_REQUESTS_PER_DOMAIN']
    DOWNLOAD_TIMEOUT = settings_detail_dic['DOWNLOAD_TIMEOUT']

    filter_redis_detail = dic['filter_redis_detail']
    filter_redis_detail_dic = eval(filter_redis_detail)
    filter_redis_detail_host = filter_redis_detail_dic['host']
    filter_redis_detail_port = filter_redis_detail_dic['post']

    mysql_detail = dic['mysql_detail']
    mysql_detail_dic = eval(mysql_detail)
    mysql_detail_host = mysql_detail_dic['host']
    mysql_detail_port = mysql_detail_dic['post']
    MYSQL_DBNAME = father_mission_name # 数据库名称设为父任务的名称
    mysql_detail_user = mysql_detail_dic['user']
    mysql_detail_password = mysql_detail_dic['password']

    mongo_detail = dic['mongo_detail']
    mongo_detail_dic = eval(mongo_detail)
    mongo_detail_host = mongo_detail_dic['host']
    mongo_detail_port = mongo_detail_dic['post']
    MONGO_DATABASE = father_mission_name # 数据库名称设为父任务的名称

    try:
        arr = (
            father_mission_name,
            spider_name,
            ROBOTSTXT_OBEY,
            COOKIES_ENABLED,
            RETRY_ENABLED,
            HTTP_PROXY_ENABLED,
            AUTOTHROTTLE_ENABLED,
            AUTOTHROTTLE_START_DELAY,
            AUTOTHROTTLE_MAX_DELAY,
            DOWNLOAD_DELAY,
            CONCURRENT_REQUESTS_PER_DOMAIN,
            DOWNLOAD_TIMEOUT,
            settings.CORE_REDIS_HOST,
            settings.CORE_REDIS_PORT,
            filter_redis_detail_host,
            filter_redis_detail_port,
            mysql_detail_host,
            mysql_detail_port,
            MYSQL_DBNAME,
            mysql_detail_user,
            mysql_detail_password,
            mongo_detail_host,
            mongo_detail_port,
            MONGO_DATABASE,
        )
        content = setting_template_of_mi % arr
        filename = os.getcwd() + '/mi/settings.py'
        with open(filename, 'w') as f:
            f.write(content)
            f.close()
    except:
        raise Exception('set settings of mi failed')
