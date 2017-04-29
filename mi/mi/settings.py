# -*- coding: utf-8 -*-

BOT_NAME = 'mi'

SPIDER_MODULES = ['mi.spiders']
NEWSPIDER_MODULE = 'mi.spiders'

#配置
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = False  #禁止COOKIES
RETRY_ENABLED = False   #禁止重试
DOWNLOAD_TIMEOUT = 30   #超时时限
DOWNLOAD_DELAY = 0.6   #间隔时间
#DEPTH_LIMIT = 20 #爬取深度,20是为了避免那些动态生成链接的网站造成的死循环,暂时没遇到这种网站,先禁用了

# mongodb
MONGO_URI = 'mongodb://192.168.139.239:27017'
MONGO_DATABASE = 'mi'
MONGO_COLLECTION_NAME = "date_20170410_F"

# redis —— url存储
REDIS_HOST = '192.168.139.239'
REDIS_PORT = 7001
# redis —— 去重队列
FILTER_HOST = '192.168.139.239'
FILTER_PORT = 7001
FILTER_DB = 0

#日志设置,禁用“LOG_STDOUT=True”
#LOG_FILE='mi.log'
#LOG_LEVEL='INFO'

#pipelines 从300累加
ITEM_PIPELINES = {
    'mi.pipelines.MongoPipeline':301,
}

#中间件
DOWNLOADER_MIDDLEWARES = {
    'mi.rotateUserAgentMiddleware.RotateUserAgentMiddleware': 400,
}


#和代理有关的中间件,暂未实现
'''
SPIDER_MIDDLEWARES = {
    'mi.myProxyMiddlewares.MyProxyMiddleware': 100,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110
}
'''

SCHEDULER = "mi.scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'mi.scrapy_redis.queue.SpiderPriorityQueue'

#自定义命令
COMMANDS_MODULE = 'mi.commands'


#没有这个会出现异常
DOWNLOAD_HANDLERS = {'s3': None,}

#huxiu——虎嗅
huxiu_base_url = 'https://www.huxiu.com'
huxiu_start_urls='huxiu:start_urls'
huxiu_dupefilter='huxiu:dupefilter'
huxiu_requests='huxiu:requests'

#huaerjie——华尔街
huaerjie_base_url = 'https://wallstreetcn.com'
huaerjie_start_urls='huaerjie:start_urls'
huaerjie_dupefilter='huaerjie:dupefilter'
huaerjie_requests='huaerjie:requests'

#caijing——财经
caijing_base_url='http://www.caijing.com.cn'
caijing_start_urls='caijing:start_urls'
caijing_dupefilter='caijing:dupefilter'
caijing_requests='caijing:requests'

#fenghuang——凤凰网
fenghuang_base_url='http://news.ifeng.com/'
fenghuang_start_urls='fenghuang:start_urls'
fenghuang_dupefilter='fenghuang:dupefilter'
fenghuang_requests='fenghuang:requests'

#souhu——搜狐网
souhu_base_url='http://news.sohu.com/'
souhu_start_urls='souhu:start_urls'
souhu_dupefilter='souhu:dupefilter'
souhu_requests='souhu:requests'

#wangyi——网易新闻
wangyi_base_url='http://news.163.com/'
wangyi_start_urls='wangyi:start_urls'
wangyi_dupefilter='wangyi:dupefilter'
wangyi_requests='wangyi:requests'