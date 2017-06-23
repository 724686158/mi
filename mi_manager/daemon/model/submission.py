# -*- coding: utf-8 -*-
from mi_manager.daemon.model.task import Task
class Submisson(object):
    def __init__(self, name, detail, fathermission_name, resource_dic, weight):
        self.submission_name = name # 此值是子任务的唯一标志, 它是父任务名+爬虫名
        self.fathermission_name = fathermission_name
        self.resource_dic = resource_dic
        self.spider_name = detail['spider_name']
        self.settings_name = detail['settings']
        self.priority = float(detail['priority']) * float(weight)
        self.start_url = detail['start_url']

    def create_task_with_submission_infomathon(self):
        task = Task(self.spider_name, self.resource_dic, self.settings_name, self.fathermission_name)






