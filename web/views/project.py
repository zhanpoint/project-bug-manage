from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from web.forms.project import NewProjectModelForm
from web import models
from utils.aliyun import oss
import oss2


def project(request):
    if request.method == 'POST':
        form = NewProjectModelForm(request, data=request.POST)
        if form.is_valid():
            newproject = form.save(commit=False)
            # 由于该字段newproject.leader没有默认值，需要指定是哪个用户创建项目
            newproject.leader = request.bugtracer.user

            # 为新建项目创建对应的oss桶
            """
            阿里云 OSS 的命名规范:
                 1. 只能包含小写字母、数字和短横线(-)
                 2. 必须以小写字母或者数字开头和结尾
                 3. 长度必须在3-63字节之间
            """
            bucket_name = f"bugtracer---{newproject.project_name}"
            newproject.bucket_name = bucket_name
            region = 'cn-wuhan-lr'
            oss.create_bucket_with_cors(bucket_name, region, [
                'http://127.0.0.1:8004', ], ['GET', 'POST', 'PUT', ])

            newproject.save()

            return JsonResponse({'status': True})
        else:
            return JsonResponse({'status': False, 'error': form.errors})
    else:
        # 获取项目列表
        project_dict = {'star': [], 'create': [], 'join': []}
        create_project = models.Project.objects.filter(leader=request.bugtracer.user)
        join_project = models.ProjectMember.objects.filter(member=request.bugtracer.user)
        for p in create_project:
            if p.star:
                # 在添加星标时，需要知道项目是我创建的还是我参与的，以便于取消星标时使用，所以需要origin字段
                project_dict['star'].append({'project_obj': p, 'origin': 'create'})
            else:
                project_dict['create'].append(p)
        for j in join_project:
            if j.star:
                project_dict['star'].append({'project_obj': j, 'origin': 'join'})
            else:
                project_dict['join'].append(j)

        form = NewProjectModelForm(request)
        return render(request, 'web/project.html', {'form': form, 'project_dict': project_dict})


def project_addstar(request):  # 添加星标
    if request.method == 'GET':
        project_type, project_id = request.GET.get('project_type'), request.GET.get('project_id')
        if project_type == 'create':
            models.Project.objects.filter(id=project_id, leader=request.bugtracer.user).update(star=True)
            return JsonResponse({'status': True})
        elif project_type == 'join':
            models.ProjectMember.objects.filter(project_id=project_id, member=request.bugtracer.user).update(star=True)
            return JsonResponse({'status': True})
        else:
            return JsonResponse({'status': False})


def project_cancelstar(request):  # 取消星标
    if request.method == 'GET':
        project_type, project_id = request.GET.get('project_type'), request.GET.get('project_id')
        if project_type == 'create':
            models.Project.objects.filter(id=project_id, leader=request.bugtracer.user).update(star=False)
            return JsonResponse({'status': True})
        elif project_type == 'join':
            models.ProjectMember.objects.filter(project_id=project_id, member=request.bugtracer.user).update(star=False)
            return JsonResponse({'status': True})
        else:
            return JsonResponse({'status': False})
