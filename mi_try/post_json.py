# -*- coding: utf-8 -*-

# 用于生成json文件, 这些json可用于开启容器
import requests
import os

data = '''{
  "id": "mission1jdcommiv8",
  "cmd": null,
  "cpus": 1,
  "mem": 256,
  "disk": 256,
  "instances": 1,
  "container": {
    "docker": {
      "image": "mi:v8",
      "network": "HOST",
      "parameters": []
    },
    "type": "DOCKER",
    "volumes": []
  }
}
'''
url = 'http://122.114.62.116:8080/v2/apps'
headers = {'Authorization' : '(some auth code)', 'Content-Type' : 'application/json'}
response = requests.post(url, data=open(os.getcwd() + '/jsons/mi.json', 'rb'), headers=headers)
print response.content