# -*- coding: utf-8 -*-

class Task(object):

    def __init__(self, spider_name, resource_dic, settings_name, father_mission_name, start_url):
        self.spider_name = spider_name
        self.core_reids = resource_dic.get('core_reids')
        self.filter_redis = resource_dic.get('filter_redis')
        self.mongo = resource_dic.get('mongo')
        self.mysql = resource_dic.get('mysql')
        self.father_mission_name = father_mission_name
        self.settings_name = settings_name
        self.start_url = start_url