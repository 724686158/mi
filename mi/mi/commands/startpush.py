# -*- coding: utf-8 -*-
import redis
import settings as settings
class StartPush(object):
    #框架在dupefilter的部分有bug，产生的redis队列在名字的末尾多一个0.暂时先手动加着
    def push(self):
        print "pushing start_url......"
        try:
            r = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT)
            # huxiu
            r.delete(settings.huxiu_start_urls)
            r.delete(settings.huxiu_dupefilter + '0')
            r.delete(settings.huxiu_requests)
            r.lpush(settings.huxiu_start_urls, settings.huxiu_base_url)

            # caijing
            r.delete(settings.caijing_start_urls)
            r.delete(settings.caijing_dupefilter + '0')
            r.delete(settings.caijing_requests)
            r.lpush(settings.caijing_start_urls, settings.caijing_base_url)

            # huaerjie
            r.delete(settings.huaerjie_start_urls)
            r.delete(settings.huaerjie_dupefilter + '0')
            r.delete(settings.huaerjie_requests)
            r.lpush(settings.huaerjie_start_urls, settings.huaerjie_base_url)

            #fenghuang
            r.delete(settings.fenghuang_start_urls)
            r.delete(settings.fenghuang_dupefilter + '0')
            r.delete(settings.fenghuang_requests)
            r.lpush(settings.fenghuang_start_urls, settings.fenghuang_base_url)

            #souhu
            r.delete(settings.souhu_start_urls)
            r.delete(settings.souhu_dupefilter + '0')
            r.delete(settings.souhu_requests)
            r.lpush(settings.souhu_start_urls, settings.souhu_base_url)

            #wangyi
            r.delete(settings.wangyi_start_urls)
            r.delete(settings.wangyi_dupefilter + '0')
            r.delete(settings.wangyi_requests)
            r.lpush(settings.wangyi_start_urls, settings.wangyi_base_url)

            print "pushing start_url success"
        except Exception:
            print "pushing start_url failed"