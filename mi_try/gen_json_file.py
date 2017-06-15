# -*- coding: utf-8 -*-
import os

# 用于创建新容器的json的模板
json_template = \
'''\
{
  "id": "%smiv8",
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
# 传入爬虫子任务名
def generate_json(submission_name):
    try:
        arr = (submission_name)
        content = json_template % arr
        filename = os.getcwd() + '/jsons/'+ submission_name  + '.json'
        with open(filename, 'w') as f:
            f.write(content.encode('utf8'))
            print 'success'
        return True
    except:
        print 'fall'
        return False
    finally:
        f.close()

if __name__ == '__main__':
    generate_json('mission1jdcom')