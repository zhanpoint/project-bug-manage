from django import template
from django.urls import reverse
from web import models

register = template.Library()


@register.inclusion_tag('inclusion_tag/navigate_project_list.html')
def navigate_project_list(request):
    create_project_list = models.Project.objects.filter(leader=request.bugtracer.user)
    join_project_list = models.ProjectMember.objects.filter(member=request.bugtracer.user)
    # 不要忘记向 inclusion_tag 传递request等参数
    return {'create': create_project_list, 'join': join_project_list, 'request': request}


@register.inclusion_tag('inclusion_tag/project_manage_menu.html')
def project_manage_menu(request):
    data_list = [
        {'name': '概览', 'url': reverse("web:dashboard", kwargs={'project_id': request.bugtracer.project.id})},
        {'name': '问题', 'url': reverse("web:issue", kwargs={'project_id': request.bugtracer.project.id})},
        {'name': '统计', 'url': reverse("web:statistic", kwargs={'project_id': request.bugtracer.project.id})},
        {'name': 'wiki', 'url': reverse("web:wiki", kwargs={'project_id': request.bugtracer.project.id})},
        {'name': '文件', 'url': reverse("web:file", kwargs={'project_id': request.bugtracer.project.id})},
        {'name': '设置', 'url': reverse("web:projectsetting", kwargs={'project_id': request.bugtracer.project.id})},
    ]
    for item in data_list:
        if request.path_info.startswith(item['url']):
            item['class'] = 'active'
    return {'data_list': data_list}
