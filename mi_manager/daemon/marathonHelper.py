# -*- coding: utf-8 -*-
import requests
class MarathonHelper():
    def __init__(self):
        self.left = 6
        self.now = 0
        self.container_list = []
    # 计算剩余负载能力 (待完善)
    def permit_container_number(self, need_cpu, need_mem, need_disk):
        return 1
        #return self.left - self.now

    def post_json_to_marathon(self, url, file, container):
        try:
            headers = {'Authorization': '(some auth code)', 'Content-Type': 'application/json'}
            response = requests.post(url, data=open(file, 'rb'), headers=headers)
            self.container_list.append(container)
            self.left = self.left - 1
            print '[Marathon]', '已收到指令,正在创建新容器'
            #print response.content
        except:
            pass
            #print '向marathon发post请求失败'

