import json
from web import models
from django import conf
import subprocess

class MultiTaskManager(object):
    def __init__(self,request):
        self.request = request
        self.run_task()

    def task_parser(self):
        self.task_data = json.loads(self.request.POST.get('task_data'))
        # selected_host_id = self.request.get('selected_hosts')
        task_type = self.task_data.get('task_type')
        # cmd = self.request.get('cmd')
        # print('cmd',cmd)

        if hasattr(self,task_type):
            func = getattr(self,task_type)
            func()
        else:
            print('cannot find task',task_type)

    def run_task(self):

        self.task_parser()

    def cmd(self):
        # 生成数据库记录，拿到了任务id
        task_obj = models.Task.objects.create(
            task_type='cmd',
            content=self.task_data.get('cmd'),
            user = self.request.user,
        )


        #触发任务，任务结果先初始化写到数据库，每个子任务执行完后更新结果（解决执行200台，执行一半时断网了，后面的
        #不执行，任务结果没写数据库，前端拿不到结果的问题）

        #初始化子记录
        selected_host_ids = self.task_data.get('selected_hosts')
        task_log_objs = []
        for id in selected_host_ids:
            task_log_objs.append(
                models.TaskLogDetail(  #直接生成对象，而不是objects.create写数据库
                    task = task_obj,
                    host_to_remote_user_id=id,
                    result='init',
                )
            )

        models.TaskLogDetail.objects.bulk_create(task_log_objs)

        #触发任务
        task_script = 'python %s/backend/task_runner.py %s' % (conf.settings.BASE_DIR,task_obj.id)
        cmd_process = subprocess.Popen(task_script,shell=True)

        # self.task_id = task_obj.id
        self.task_obj = task_obj
        # return task_obj.id

        print('running batch commands...')
        print('runner task obj',task_obj)
        print(type(task_obj))