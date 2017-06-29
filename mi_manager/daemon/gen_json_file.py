# -*- coding: utf-8 -*-
import os
import settings

# 用于创建新容器的json的模板
json_template = \
'''\
{
  "id": "/spiders/%s%s",
  "cmd": null,
  "cpus": %s,
  "mem": %s,
  "disk": %s,
  "instances": 1,
  "container": {
    "docker": {
      "image": "mi:v10",
      "network": "HOST",
      "parameters": []
    },
    "type": "DOCKER",
    "volumes": []
  }
}
'''
# 传入爬虫子任务名
def generate_json(mission_name, container_name, cpu, mem, disk):
    try:
        arr = (mission_name, container_name,cpu, mem, disk)
        content = json_template % arr
        filename = os.getcwd() + settings.TEMP_PATH + '/jsons/'+ mission_name + container_name  + '.json'
        with open(filename, 'w') as f:
            f.write(content)
            f.close()
    except:
        print 'fall'