from django.shortcuts import render

from web import models
from web.forms.file import FileModelForm
from django.http import JsonResponse


def file(request, project_id):
    # 添加文件夹
    if request.method == 'POST':
        # 获取父文件夹ID,默认为0
        parent_obj = None
        folder_id = request.POST.get('folder', '')
        if folder_id and folder_id.isdigit():
            parent_obj = models.FileRepository.objects.filter(project=request.bugtracer.project, id=folder_id, )
        form = FileModelForm(data=request.POST)
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
        form = FileModelForm()
        return render(request, 'web/file.html/', {'form': form})
