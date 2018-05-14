import sys,os,json
# import django
# from web import models
import time
import paramiko
from concurrent.futures import ThreadPoolExecutor


def ssh_cmd(sub_task_obj):
    host_to_user_obj = sub_task_obj.host_to_remote_user
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
            ssh.connect(host_to_user_obj.host.ip_addrss, host_to_user_obj.host.port,
                        host_to_user_obj.remote_users.username,host_to_user_obj.remote_users.password,timeout=5)
            stdin, stdout, stderr = ssh.exec_command(sub_task_obj.task.content)
            stdout_res = stdout.read().decode('utf-8')
            stderr_res = stderr.read().decode('utf-8')
            # res = stdout_res + stderr_res
            sub_task_obj.result = stdout_res + stderr_res
            print('---------result---------',stderr_res)


            if stderr_res:
                sub_task_obj.status = 2
                # exit('excute command error')
            else:
                sub_task_obj.status = 1
            # sub_task_obj.save()
    except Exception as e:
        sub_task_obj.result = e
        sub_task_obj.status = 2
    sub_task_obj.save()
    ssh.close()

def file_transfer(sub_task_obj,task_data):
    import os, sys
    import paramiko
    from django.conf import settings
    host_to_user_obj = sub_task_obj.host_to_remote_user

    try:
        t = paramiko.Transport((host_to_user_obj.host.ip_addrss, host_to_user_obj.host.port))
        t.connect(username=host_to_user_obj.remote_users.username, password=host_to_user_obj.remote_users.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        if task_data['file_transfer_type'] == 'send':
            sftp.put(task_data['local_file_path'], task_data['remote_file_path'])
            task_result = 'file [%s] send to [%s] succeed.' % (task_data['local_file_path'],task_data['remote_file_path'])
            # sub_task_obj.status = 1
        else:
            local_file_path = settings.DOWNLOAD_DIR
            filename = task_data['remote_file_path'].split('/')[-1]
            print('-->filename',filename)
            # if not os.path.isdir(task_obj.task_id):
            #     os.mkdir(os.path.isdir(task_obj.task_id))
            if not os.path.isdir('%s/%s' % (local_file_path,task_obj.id)):
                os.mkdir('%s/%s' % (local_file_path,task_obj.id))
            sftp.get(task_data['remote_file_path'], '%s/%s/%s_%s' % (local_file_path,
                                                                     task_obj.id,
                                                                     host_to_user_obj.host.ip_addrss,
                                                                     filename))
            print('file downloads?')
            task_result = 'file [%s] download succeed' % task_data['remote_file_path']
            # sub_task_obj.status = 1
        t.close()
        sub_task_obj.status = 1
    except Exception as e:
        task_result = e
        print('-->',e)
        sub_task_obj.status = 2

    sub_task_obj.result = task_result
    sub_task_obj.save()



if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(base_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fortress.settings")
    import django
    django.setup()
    from web import models
    if len(sys.argv) == 1:
        exit('task id not provided.')
    else:
        task_id = sys.argv[1] #task_obj_id
        task_obj = models.Task.objects.get(id=task_id)
        print('task runner',type(task_obj),task_obj)

    pool = ThreadPoolExecutor(10)
    if task_obj.task_type == 'cmd':
        for sub_task_obj in task_obj.tasklogdetail_set.all():
            # pool = ThreadPoolExecutor(10)
            pool.submit(ssh_cmd,sub_task_obj)
    else:
        task_data = json.loads(task_obj.content)
        print('-->task_data',type(task_data),task_data)
        for sub_task_obj in task_obj.tasklogdetail_set.all():
            pool.submit(file_transfer,sub_task_obj,task_data)

    pool.shutdown(wait=True)

