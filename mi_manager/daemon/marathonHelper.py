# -*- coding: utf-8 -*-
import requests

# 计算剩余负载能力 (待完善)
def permit_container_number(need_cpu, need_mem, need_disk):
    return 2

def post_json_to_marathon(url, file):
    headers = {'Authorization': '(some auth code)', 'Content-Type': 'application/json'}
    response = requests.post(url, data=open(file, 'rb'), headers=headers)
    print response.content


