# -*- coding: utf-8 -*-

# 调整电商类的start_url
def get_start_url(spider_name, start_url):
    if spider_name == 'amazon.cn':
        start_url = 'https://www.amazon.cn/%E6%95%B0%E7%A0%81%E5%BD%B1%E9%9F%B3/dp/B014KP76G6/ref=sr_1_4?s=pc&ie=UTF8&qid=1493610822&sr=1-4&keywords=fire%E5%B9%B3%E6%9D%BF&th=1'
    elif spider_name == 'dangdang.com':
        start_url = 'http://www.dangdang.com'
    elif spider_name == 'gome.com.cn':
        start_url = 'http://www.gome.com.cn'
    elif spider_name == 'taobao.com':
        start_url = 'https://www.taobao.com'
    elif spider_name == 'tmall.com':
        start_url = 'https://www.taobao.com'
    elif spider_name == 'jd.com':
        if 'item' in start_url:
            pass
        else:
            start_url = 'https://item.jd.com/3312381.html'
    return start_url
