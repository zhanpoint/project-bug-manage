from django.shortcuts import render


def dashboard(request, project_id):
    return render(request, 'web/dashboard.html/')


def issue(request, project_id):
    return render(request, 'web/issue.html/')


def statistic(request, project_id):
    return render(request, 'web/statistic.html/')


def file(request, project_id):
    return render(request, 'web/file.html/')


def wiki(request, project_id):
    return render(request, 'web/wiki.html/')


def setting(request, project_id):
    return render(request, 'web/setting.html/')
