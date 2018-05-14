
import sys,json,subprocess
from web import models
from django import conf
import json

class MultiTaskManager(object):
    def __init__(self,request):
        self.request = request
        self.task_run()

    def task_parse(self):
        self.task_data = json.loads(self.request.POST.get('task_data'))
        print('-----------task_parse---------task_data ',self.task_data,type(self.task_data))
        print('-----------task_parse---------json.dumps---task_data ', json.dumps(self.task_data),type(json.dumps(self.task_data)))
        task_type = self.task_data.get('task_type')
        # if sys.argv == 1:
        #     return 'ok'
        if hasattr(self,task_type):
            task_func = getattr(self,task_type)
            task_func()
        else:
            print('cannot find method %s' % task_type)


    def task_run(self):

        self.task_parse()

    def cmd(self):
        task_obj = models.Task.objects.create(task_type='cmd',
        content = self.task_data.get('cmd'),
        user = self.request.user,)

        selected_host_ids = set(self.task_data['selected_hosts'])
        task_log_objs = []
        for id in selected_host_ids:
            task_log_objs.append(
                models.TaskLogDetail(task=task_obj,
                                     host_to_remote_user_id=id,
                                     result='init',
                                     )
            )
        print('task_log_objs-->',task_log_objs)
        models.TaskLogDetail.objects.bulk_create(task_log_objs)
        task_script = 'python %s/backend/task_runner.py %s' % (conf.settings.BASE_DIR, task_obj.id)
        cmd_process = subprocess.Popen(task_script, shell=True)

        print('running batch commands...')

        # self.task_id = task_obj.id
        self.task_obj = task_obj

    def file_transfer(self):
        task_obj = models.Task.objects.create(task_type='file-transfer',
        content = json.dumps(self.task_data),
        user = self.request.user,)

        selected_host_ids = set(self.task_data['selected_hosts'])
        task_log_objs = []
        for id in selected_host_ids:
            task_log_objs.append(
                models.TaskLogDetail(task=task_obj,
                                     host_to_remote_user_id=id,
                                     result='init',
                                     )
            )
        print('task_log_objs-->',task_log_objs)
        models.TaskLogDetail.objects.bulk_create(task_log_objs)
        task_script = 'python %s/backend/task_runner.py %s' % (conf.settings.BASE_DIR, task_obj.id)
        cmd_process = subprocess.Popen(task_script, shell=True)

        print('running batch commands...')

        # self.task_id = task_obj.id
        self.task_obj = task_obj
