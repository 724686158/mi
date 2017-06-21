# -*- coding: utf-8 -*-
import redis
import settings
if __name__ == '__main__':
    r = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, settings.SUBMISSION_DB)
    r.set('mission1_jd.com', '{"spider_name": "jd.com","father_mission_name": "mission1","settings": "默认设置1","priority": 5}')

    r = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, settings.MISSION_DB)
    r.set('任务1', "{'submission_list': [{'name': 'mission1_jd.com', 'detail': {'spider_name': 'jd.com', 'settings': '默认设置1', 'priority': 2}}], 'weight': 0.8, 'start_time': 1498030984.74, 'resource_dic': {}, 'state': 'START', 'end_time': 1498031000.74}")
