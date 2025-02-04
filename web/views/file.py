from django.shortcuts import render

from web import models
from web.forms.file import FileModelForm
from django.http import JsonResponse


def file(request, project_id):
    parent_obj = None
    folder_id = request.GET.get('folder', '')
    if folder_id and folder_id.isdigit():
        parent_obj = models.FileRepository.objects.filter(project=request.bugtracer.project, id=folder_id, file_type=2)
    # 添加文件夹
    if request.method == 'POST':
        # 获取父文件夹ID,默认为空字符串

        form = FileModelForm(request, parent_obj, data=request.POST)
        if form.is_valid():
            form.instance.project = request.bugtracer.project
            form.instance.file_type = 2
            form.instance.update_user = request.bugtracer.user
            form.instance.parent = parent_obj
            form.save()
            return JsonResponse({'status': True})
        else:
            return JsonResponse({'status': False, 'error': form.errors})
    else:
        # 获取当前目录下的文件列表（所有的文件夹和文件）
        form = FileModelForm(request, parent_obj, )
        queryset = models.FileRepository.objects.filter(project=request.bugtracer.project)
        if parent_obj:
            file_list = queryset.filter(parent=parent_obj).order_by('-file_type')
        else:
            file_list = queryset.filter(parent__isnull=True).order_by('-file_type')
        return render(request, 'web/file.html/', {'form': form, 'file_list': file_list})
