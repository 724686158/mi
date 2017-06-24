# -*- coding: utf-8 -*-
import os
import redis
import mi_manager.daemon.settings as settings
import gen_json_file
import time
Time = lambda: time.strftime('%Y%m%d%H%M%S')

from mi_manager.daemon.model.mission import Mission

def get_redis(db_id):
    return redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, db_id)

def get_resource(type, name):
    if type == 'Redis':
        r = get_redis(settings.RESOURCES_REDIS_DB)
        return r.get(name)
    if type == 'Mysql':
        r = get_redis(settings.RESOURCES_MYSQL_DB)
        return r.get(name)
    if type == 'Mongo':
        r = get_redis(settings.RESOURCES_MONGO_DB)
        return r.get(name)

def get_mission(name):
    r = get_redis(settings.MISSION_DB)
    return r.get(name)

def get_submission(name):
    r = get_redis(settings.SUBMISSION_DB)
    return r.get(name)

def get_settings(name):
    r = get_redis(settings.SETTINGS_DB)
    return r.get(name)

def get_spider(name):
    # 如果在新闻爬虫白名单中, 则返回数据库中存储的值, 如果不在新闻爬虫白名单中, 则返回空值
    r = get_redis(settings.SPIDERS_DB)
    return r.get(name)

def push_task(info_dic_str, priority):
    r = get_redis(settings.DISPATCH_DB)
    print r.zadd('task_zset', info_dic_str, priority)

def pop_task(number):
    ans = []
    r = get_redis(settings.DISPATCH_DB)
    tasks = r.zrange('task_zset', 0, number)
    print type(ans)

    for task in tasks:
        ans.append(task)
        r.zrem('task_zset', task)
    return ans

def check_mission_state(mission_name, start_time, end_time):
    r = get_redis(settings.DISPATCH_DB)
    # 首先检查时间是否在start_time和end_time之间
    now_time = time.time()
    # print 'now_time:' + str(now_time) + ' start_time:' + str(start_time) + ' end_time:' + str(end_time)
    if now_time >= start_time and now_time < end_time:
        info = r.zadd('mission_zset', mission_name, 0)
        if info == 1:
            print '任务：' + mission_name + ' 开始'
            return 'READY'
        elif info == 0:
            print '任务：' + mission_name + ' 执行中'
            return 'RUNNING'
    else:
        info = r.zrem('mission_zset', mission_name)
        if info == 1:
            print '任务：' + mission_name + ' 结束'
            return 'FINISH'
        elif info == 0:
            print '任务：' + mission_name + ' 等待中'
            return 'WAIT'

def get_all_mission():
    r = get_redis(settings.MISSION_DB)
    keys = r.keys()
    missions = []
    for key in keys:
        missions.append(Mission(key, r.get(key)))
    return missions

# 用于发现任务否发生了变化
def is_missions_change():
    r = get_redis(settings.SYMBOL_DB)
    symbol = r.get('MISSIONS_CHANGE')
    if symbol == '1':
        r.set('MISSIONS_CHANGE', '0')
        return True
    else:
        return False

def save_misson(name, detail):
    r = get_redis(settings.MISSION_DB)
    r.set(name, str(detail))

def permit_container_number(marathon_helper):
    return  marathon_helper.permit_container_number(settings.NEED_CPU, settings.NEED_MEM, settings.NEED_DISK)

def run_new_container(marathon_helper ,jsonfile_name):
    marathon_helper.post_json_to_marathon(settings.MARATHON_URL + '/v2/apps', os.getcwd()  + settings.TEMP_PATH + '/jsons/'+ jsonfile_name + '.json', jsonfile_name)

def issue_tasks(tasks):
    r = get_redis(settings.TASK_DB)
    for task in tasks:
        r.lpush('ready', task)


def record_tasks(tasks):
    r = get_redis(settings.TASK_DB)
    for task in tasks:
        r.lpush('history', task)

def gen_json(container_name):
    gen_json_file.generate_json(container_name, settings.NEED_CPU, settings.NEED_MEM, settings.NEED_DISK)

def clear_dispatch():
    r = get_redis(settings.DISPATCH_DB)
    r.flushdb()
def clear_task():
    r = get_redis(settings.TASK_DB)
    r.flushdb()
