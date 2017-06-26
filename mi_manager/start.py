#-*- coding: utf-8 -*-
import os
import subprocess
import redis
import settings
import gen_settings
import time

CWD = os.getcwd()

def start_work():
    subprocess.Popen(['python', CWD + '/daemon/app.py'])  # 开启守护进程
    os.system('python ' + CWD + '/monitor/app.py')

def verify_core_redis_db():
    try:
        r = redis.Redis(settings.CORE_REDIS_HOST, settings.CORE_REDIS_PORT)
        info =  r.info()
        print '可以正确连接到核心redis数据库'
        used_mem = info['used_memory']
        print '已经使用内存：%.4f%%' % (float(used_mem) / float(settings.CORE_REDIS_MAX_MEMORY * 1024 * 1024 * 1024))
        if used_mem > settings.CORE_REDIS_MAX_MEMORY * 1024 * 1024 * 1024 * 0.8:
            print '核心数据库内存占用超过可用容量的80%（系统将自动清理可能存在的无用缓存, 请检查是否有任务将核心数据库用作缓存数据库'
            filter_db = redis.Redis(settings.CORE_REDIS_HOST, settings.CORE_REDIS_PORT, 0)
            filter_db.flushdb()
            '''
            monitor_db = redis.Redis(settings.CORE_REDIS_HOST, settings.CORE_REDIS_PORT, 15)
            monitor_db.flushdb()
            '''
        else:
            print '核心数据库状态良好'
    except:
        raise Exception('core redis db not find')

def set_settings():
    try:
        gen_settings.generate_setting_of_monitor({'APP_HOST': settings.APP_HOST, 'APP_PORT': settings.APP_PORT, 'CORE_REDIS_HOST': settings.CORE_REDIS_HOST, 'CORE_REDIS_PORT': settings.CORE_REDIS_PORT, 'TEMP_PATH': settings.MONITOR_TEMP_PATH})
        gen_settings.generate_setting_of_daemon({'MESOS_URL': settings.MESOS_URL, 'MARATHON_URL': settings.MARATHON_URL, 'CORE_REDIS_HOST': settings.CORE_REDIS_HOST, 'CORE_REDIS_PORT': settings.CORE_REDIS_PORT, 'TEMP_PATH': settings.DAEMON_TEMP_PATH})
        print '配置项设置成功'
    except:
        raise Exception('set settings failed')

def update_data():
    # 如果系统启动时 白名单爬虫列表为空, 则从文件中加载爬虫信息
    try:
        r = redis.Redis(settings.CORE_REDIS_HOST, settings.CORE_REDIS_PORT, db=settings.SPIDERS_DB)
        keys = r.keys()
        if len(keys) == 0:
            filename = "spider_whitelist.txt"
            with open(filename, 'r') as f:
                key = f.readline()
                while key.__len__() > 0:
                    key = key.split('\n')[0]
                    print key
                    info = f.readline().split('\n')[0]
                    r.set(key, info)
                    key = f.readline()
                    if key.__len__() < 2:
                        key = f.readline()
            print '自动加载精准新闻爬虫'
    except:
        raise Exception('loading spider data failed')
    # 如果系统中没有可用的资源
    r = redis.Redis(settings.CORE_REDIS_HOST, settings.CORE_REDIS_PORT, db=settings.RESOURCES_REDIS_DB)
    #r.flushdb()
    keys = r.keys()
    if len(keys) == 0:
        r.set("useful_redis", "{'host': '122.114.62.116', 'password': '', 'post': '7001', 'user': ''}")
    r = redis.Redis(settings.CORE_REDIS_HOST, settings.CORE_REDIS_PORT, db=settings.RESOURCES_MYSQL_DB)
    #r.flushdb()
    keys = r.keys()
    if len(keys) == 0:
        r.set("useful_mysql", "{'host': '122.114.62.116', 'password': 'mi', 'post': '3306', 'user': 'root'}")
    r = redis.Redis(settings.CORE_REDIS_HOST, settings.CORE_REDIS_PORT, db=settings.RESOURCES_MONGO_DB)
    #r.flushdb()
    keys = r.keys()
    if len(keys) == 0:
        r.set("useful_mongo", "{'host': '122.114.62.116', 'password': '', 'post': '27017', 'user': ''}")

    # 如果系统中没有合适的设置
    r = redis.Redis(settings.CORE_REDIS_HOST, settings.CORE_REDIS_PORT, db=settings.SETTINGS_DB)
    #r.flushdb()
    keys = r.keys()
    if len(keys) == 0:
        r.set("新闻类爬虫默认配置", "{'AUTOTHROTTLE_MAX_DELAY': '6', 'ROBOTSTXT_OBEY': False, 'CONCURRENT_REQUESTS_PER_DOMAIN': '10', 'RETRY_ENABLED': True, 'AUTOTHROTTLE_START_DELAY': '1', 'AUTOTHROTTLE_ENABLED': True, 'DOWNLOAD_TIMEOUT': '10', 'COOKIES_ENABLED': True, 'HTTP_PROXY_ENABLED': False, 'DOWNLOAD_DELAY': '2'}")
        r.set("电商类爬虫默认配置", "{'AUTOTHROTTLE_MAX_DELAY': '6', 'ROBOTSTXT_OBEY': False, 'CONCURRENT_REQUESTS_PER_DOMAIN': '20', 'RETRY_ENABLED': False, 'AUTOTHROTTLE_START_DELAY': '1', 'AUTOTHROTTLE_ENABLED': True, 'DOWNLOAD_TIMEOUT': '10', 'COOKIES_ENABLED': True, 'HTTP_PROXY_ENABLED': False, 'DOWNLOAD_DELAY': '1'}")

    # 如果系统中没有合适的设置
    r = redis.Redis(settings.CORE_REDIS_HOST, settings.CORE_REDIS_PORT, db=settings.SYMBOL_DB)
    r.flushdb()
    keys = r.keys()
    if len(keys) == 0:
        r.set('mesos_url', settings.MESOS_URL)
        r.set('marathon_url', settings.MARATHON_URL)
    # 设置开始时间
    r.set('system_start_time', time.time())

    # 重置电商类白名单
    r = redis.Redis(settings.CORE_REDIS_HOST, settings.CORE_REDIS_PORT, db=settings.CLASSIFIER_DB)
    r.delete('known_ecommerce')


if __name__ == '__main__':
    # 首先确认核心数据库可用
    verify_core_redis_db()

    # 整理模块设置
    set_settings()

    # 收集可能变更的数据, 更新数据库
    update_data()


    # 正式开始工作
    start_work()
    try:
        pass
    except Exception, e:
        print '[error]: ' + e.args[0]

