from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
import json
from web import models
from backend.multitask import MultiTaskManager
# Create your views here.

@login_required
def dashboard(request):

    return render(request,'index.html')

def acc_login(request):
    error_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('/')
        else:
            error_msg = 'Wrong username or password.'
            # return redirect('/acc_login')
    return render(request,'login.html',{'error_msg':error_msg})

def web_ssh(request):

    return render(request,'web_ssh.html')

@login_required
def host_mgr(request):

    return render(request,'host_mgr.html')

@login_required
def file_transfer(request):

    return render(request,'file_transfer.html')

@login_required
def batch_task_mgr(request):

    # print(request.POST)
    task_data = json.loads(request.POST.get('task_data'))
    print('task_data',task_data)
    task_obj = MultiTaskManager(request)
    print('task obj',task_obj)
    print(type(task_obj))
    # print(type(task_obj.task_obj))
    # print(task_obj.task_obj.id)
    # task_id = task_obj.id
    response = {
        'task_id':task_obj.task_obj.id,
        'selected_obj':list(task_obj.task_obj.tasklogdetail_set.all().values('id','host_to_remote_user__host__name',
                                                            'host_to_remote_user__host__ip_addrss',
                                                            'result',
                                                            'status'))
    }
    return HttpResponse(json.dumps(response))

def task_result(request):
    task_id = request.GET.get('task_id')
    sub_task_objs = models.TaskLogDetail.objects.all().filter(task_id=task_id)
    print('sub_task_objs',sub_task_objs)
    log_data = list(sub_task_objs.values('id','status','result'))

    return HttpResponse(json.dumps(log_data))

def tmp(request):

    return render(request,'tmp.html')


