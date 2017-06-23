# -*- coding: utf-8 -*-
class Mission(object):
    '''
    def __init__(self, mission_name, start_time, end_time, submission_list, resource_dic, weight, state):
        self.mission_name = mission_name
        self.start_time = start_time
        self.end_time = end_time
        self.submission_list = submission_list
        self.resource_dic = resource_dic
        self.weight = weight
        self.state = state
    '''


    def __init__(self, name, detail):
        dic = eval(detail)
        self.mission_name = name
        self.start_time = dic['start_time']
        self.end_time = dic['end_time']
        self.submission_list = list(dic['submission_list'])
        self.resource_dic = dic['resource_dic']
        self.weight = dic['weight']
        self.state = dic['state']

    def get_detail(self):
        dic = {}
        dic['start_time'] = self.start_time
        dic['end_time'] = self.end_time
        dic['submission_list'] = self.submission_list
        dic['resource_dic'] = self.resource_dic
        dic['weight'] = self.weight
        dic['state'] = self.state
        return dic

    def get_submission_list(self):
        return self.submission_list

    def get_resource_dic(self):
        return self.resource_dic


    def get_name(self):
        return self.mission_name

    def set_all_submission(self):
        pass