#-*- coding: utf-8 -*-
import time
import data_service

from mi_manager.daemon.model.mission import Mission
from mi_manager.daemon.model.submission import Submisson
from mi_manager.daemon.model.task import Task
Time = lambda: time.strftime('%Y-%m-%d %H:%M:%S')

# 任务列表
missions = []
# 子任务列表
submissions = []
# task别表
tasks = []
def test():
    mission1 = Mission('任务1', '{"start_time": ' + str(time.time() + 4) + ', "end_time":' + str(time.time() + 20) + ', "submission_list": [{"name": "mission1_jd.com", "detail": {"spider_name": "jd.com", "settings": "设置1", "priority": 2}}], "resource_dic":{"core_reids": "useful_redis","filter_redis": "useful_redis","mongo": "useful_mongo","mysql": "useful_mysql"}, "weight":0.8, "state": "START"}')
    mission2 = Mission('mission2', '{"start_time": ' + str(time.time() + 0) + ', "end_time":' + str(time.time() + 240) + ', "submission_list":[], "resource_dic":{}, "weight":0.8, "state": "STOP"}')
    mission3 = Mission('mission3', '{"start_time": ' + str(time.time() + 2) + ', "end_time":' + str(time.time() + 40) + ', "submission_list":[], "resource_dic":{}, "weight":0.8, "state": "START"}')
    data_service.save_misson(mission1.get_name(), mission1.get_detail())
    data_service.save_misson(mission2.get_name(), mission2.get_detail())
    data_service.save_misson(mission3.get_name(), mission3.get_detail())
    data_service.is_missions_change()

def test_about_stop():
    mission2 = Mission('mission2', '{"start_time": ' + str(time.time() + 0) + ', "end_time":' + str(
        time.time() + 240) + ', "submission_list":[], "resource_dic":{}, "weight":0.8, "state": "START"}')
    data_service.save_misson(mission2.get_name(), mission2.get_detail())
    print 'TEST_CHANGE'

if __name__ == '__main__':
    # 载入测试
    test()
    '''

    '''
    # 获取全部任务
    missions = data_service.get_all_mission()

    # 进入守护状态
    while True:

        print 'now time is:' + Time() + '(' + str(time.time()) + ')'
        # 当任务数据库中的信心发生改变时, 更新任务列表
        if data_service.is_missions_change():
            print '任务发生变化, 正在重新加载'
            missions = data_service.get_all_mission()

        # 更新任务的状态
        for mission in missions:
            # 对于停止状态的任务, 不做处理, 对于其他状态的任务, 检查任务是否改变
            if mission.state == 'STOP':
                print 'mission: ' + mission.mission_name + '处于停止状态, 请手动开启'
            else:
                mission.state = data_service.check_mission_state(mission.mission_name, mission.start_time, mission.end_time)

        # 遍历任务列表, 根据任务的状态, 做相应操作
        for mission in missions:
            # 对准备执行的任务, 获取子任务, 加入到子任务列表
            if mission.state == 'READY':
                get_submission_list = mission.get_submission_list()
                print "!" + str(type(get_submission_list))
                for submission in get_submission_list:
                    print submission
                    print "!!" + str(type(submission))
                    submissions.append(Submisson(submission['name'], submission['detail'], mission.get_name(), mission.get_resource_dic(), mission.weight))
            # 对运行中的任务, 检查他的子任务是否发生改变, 如有改变则重新加载
            elif mission.state == 'RUNNING':
                pass
            # 对完成的任务, 從隊列中去除子任務
            elif mission.state == 'FINISH':
                get_submission_list = mission.get_submission_list()
                print "!!!" + str(type(get_submission_list))
                for submission in get_submission_list:
                    print submission
                    print "!!!!" + str(type(submission))
                    #submissions.remove(Submisson(submission['name'], submission['detail'], mission.get_name(), mission.get_resource_dic(), mission.weight))
            # 对未到执行时间的任务不做处理
            elif mission.state == 'WAIT':
                pass

        # 对每个子任务, 将他产生的task存入调度队列(通过有序集合实现)中等待调度
        for submission in submissions:
            data_service.push_task(Task(submission.spider_name, submission.resource_dic, submission.settings_name, submission.fathermission_name).get_dic_str(), submission.priority)

        # 计算集群中可以开启的容器的剩余数量
        permit_container_number_of_mi = data_service.permit_container_number()
        # 根据负载能力,将最优先的N个task放入就绪队列
        tasks_ready = data_service.pop_task(permit_container_number_of_mi)
        data_service.issue_tasks(tasks_ready)

        # 向marathon发送等量的新容器请求, 这些新容器在开始运行时, 消费一个task
        '''
        for task in tasks_ready:
            print task
            # 根据task新建对应的json文件
            data_service.gen_json(task)
            # 用json文件创建新容器
            data_service.run_new_container(task)
        '''
        # 将发布过的task存入task历史记录中
        data_service.record_tasks(tasks_ready)

        time.sleep(2)
