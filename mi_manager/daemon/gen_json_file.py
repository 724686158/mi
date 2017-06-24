# -*- coding: utf-8 -*-
import os
import settings

# 用于创建新容器的json的模板
json_template = \
'''\
{
  "id": "%s",
  "cmd": null,
  "cpus": %s,
  "mem": %s,
  "disk": %s,
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
# 传入爬虫子任务名
def generate_json(container_name, cpu, mem, disk):
    try:
        arr = (container_name,cpu, mem, disk)
        content = json_template % arr
        filename = os.getcwd() + settings.TEMP_PATH + '/jsons/'+ container_name  + '.json'
        with open(filename, 'w') as f:
            f.write(content)
            print 'success'
            f.close()
    except:
        print 'fall'