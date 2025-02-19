from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from web.forms.issue import IssueModelForm

from web import models


def issue(request, project_id):
    # 获取项目
    project = models.Project.objects.get(id=project_id)
    if request.method == 'GET':
        form = IssueModelForm()

        # 获取所有用户
        users = models.UserInfo.objects.filter(
            # 项目负责人
            Q(id=project.leader.id) |
            # 项目成员
            Q(id__in=models.ProjectMember.objects.filter(project=project).values('member_id'))
        ).distinct()

        context = {
            'project_members': users,
            'form': form
        }
        return render(request, 'web/issue.html', context)


def issue_create(request, project_id):
    if request.method == 'POST':
        # 处理tags字段 - 因为tags是多选的，需要特殊处理
        tags = request.POST.getlist('tags')

        form = IssueModelForm(data=request.POST, files=None)
        if form.is_valid():
            issue_obj = form.save(commit=False)
            issue_obj.creator = request.bugtracer.user
            issue_obj.project = models.Project.objects.get(id=project_id)
            issue_obj.save()

            # 明确处理tags
            if tags:
                tag_objects = models.IssueTag.objects.filter(name__in=tags)
                issue_obj.tags.set(tag_objects)  # 使用set()方法设置多对多关系

            return JsonResponse({'status': True})
        # 表单验证失败
        return JsonResponse({'status': False, 'errors': form.errors})
    return JsonResponse({'status': False, 'message': '方法不允许'})
