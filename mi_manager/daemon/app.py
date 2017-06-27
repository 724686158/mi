#-*- coding: utf-8 -*-
import time
import data_service
from marathonHelper import MarathonHelper
from mi_manager.daemon.model.mission import Mission
from mi_manager.daemon.model.submission import Submisson
from mi_manager.daemon.model.task import Task
Time = lambda: time.strftime('%Y-%m-%d %H:%M:%S')



if __name__ == '__main__':
    # 从数据库中加载任务
    missions = data_service.get_all_mission()
    # 清空调度队列
    data_service.clear_dispatch()
    # 清空task缓存
    data_service.clear_task()
    # 获取marathon帮助
    marathon_helper = MarathonHelper()
    # 进入守护状态
    while True:
        try:
            print 'now time is:' + Time()
            # 更新任务列表
            if data_service.is_missions_change():
                print '任务信息发生改变, 重新加载任务队列'
                missions = data_service.get_all_mission()

            # 更新任务的状态
            for mission in missions:
                # 对于停止状态的任务, 不做处理, 对于其他状态的任务, 检查任务是否改变
                if mission.state == 'STOP':
                    print '任务: ' + mission.mission_name + '处于停止状态'
                else:
                    mission.state = data_service.check_mission_state(mission.mission_name, mission.start_time, mission.end_time)

            # 遍历任务列表, 根据任务的状态, 做相应操作
            # 清空子任务列表
            submissions = []
            for mission in missions:
                # 对准备执行的任务, 获取子任务, 加入到子任务列表
                if mission.state == 'READY':
                    get_submission_list = mission.get_submission_list()
                    for submission in get_submission_list:
                        submissions.append(Submisson(submission['name'], submission['detail'], mission.get_name(), mission.get_resource_dic(), mission.weight))
                # 对运行中的任务, 获取子任务, 加入到子任务列表
                elif mission.state == 'RUNNING':
                    get_submission_list = mission.get_submission_list()
                    for submission in get_submission_list:
                        submissions.append(Submisson(submission['name'], submission['detail'], mission.get_name(),
                                                     mission.get_resource_dic(), mission.weight))
                    pass
                # 对完成的任务, 不做处理
                elif mission.state == 'FINISH':
                    pass
                # 对未到执行时间的任务不做处理
                elif mission.state == 'WAIT':
                    pass

            # 对每个子任务, 将他产生的task存入调度队列(通过有序集合实现)中等待调度
            for submission in submissions:
                data_service.clear_submission_zset()
                data_service.push_submission(str(
                    {'father_mission_name': submission.fathermission_name, 'spider_name': submission.spider_name}), submission.priority)

                task = Task(submission.spider_name, submission.resource_dic, submission.settings_name, submission.fathermission_name, submission.start_url)
                # 下列代码根据task中的信息, 自动补全其他必要信息
                dic = {}
                dic["spider_name"] = task.spider_name
                dic["spider_detail"] = data_service.get_spider(task.spider_name)
                dic["father_mission_name"] = task.father_mission_name
                dic["settings_name"] = task.settings_name
                if dic["settings_name"]:
                    dic["settings_detail"] = data_service.get_settings(dic["settings_name"])
                dic["core_reids"] = task.core_reids
                if dic["core_reids"]:
                    dic["core_reids_detail"] = data_service.get_resource('Redis', dic["core_reids"])
                dic["filter_redis"] = task.filter_redis
                if dic["filter_redis"]:
                    dic["filter_redis_detail"] = data_service.get_resource('Redis', dic["filter_redis"])
                dic["mongo"] = task.mongo
                if dic["mongo"]:
                    dic["mongo_detail"] = data_service.get_resource('Mongo', dic["mongo"])
                dic["mysql"] = task.mysql
                if dic["mysql"]:
                    dic["mysql_detail"] = data_service.get_resource('Mysql', dic["mysql"])
                dic["father_mission_name"] = task.father_mission_name
                dic["start_url"] = task.start_url
                # 向有序队列中压入完整的task信息, 分值是对应子任务的优先度
                data_service.push_task(str(dic), submission.priority)

            # 对一个处理过的任务, 要将其权重下降40%, 直到任务队列出现变化, 重新从数据库中加载任务
            for mission in missions:
                mission.weight = str(float(mission.weight) * 0.6)

            # 计算集群中可以开启的容器的剩余数量
            permit_container_number_of_mi = data_service.permit_container_number(marathon_helper)
            # 根据负载能力,将最优先的N个task放入就绪队列
            tasks_ready = data_service.pop_task(permit_container_number_of_mi)
            data_service.issue_tasks(tasks_ready)

            # 向marathon发送等量的新容器请求, 这些新容器在开始运行时, 消费一个task
            for task in tasks_ready:
                detail_dic = eval(task)
                container_name = str(detail_dic['spider_name']).replace('.', '').replace('_', '').replace('-', '').replace(' ', '')

                # 根据task新建对应的json文件
                data_service.gen_json(detail_dic['father_mission_name'], container_name)

                # 用json文件创建新容器
                data_service.run_new_container(marathon_helper, container_name)

            # 将发布过的task存入task历史记录中
            data_service.record_tasks(tasks_ready)
        except:
            print '守护进程此轮操作出错'
        try:
            time.sleep(2)
        except:
            print '守护进程关闭'