# -*- coding: utf-8 -*-
import requests
import settings
import urllib2

class MesosHelper():
    def __init__(self):
        self.index = settings.MESOS_URL + '/#/'
        self.agent = settings.MESOS_URL + '/#/agents'


    def get_and_save_infos(self):
        req = urllib2.Request(self.index)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        print res


if __name__ == '__main__':
    mesoshelper = MesosHelper()
    print mesoshelper.get_and_save_infos()