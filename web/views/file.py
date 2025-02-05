from django.shortcuts import render

from web import models
from web.forms.file import FileModelForm
from django.http import JsonResponse


def file(request, project_id):
    """文件管理"""

    # 获取当前显示列表的父级文件夹对象
    parent_obj = None
    folder_id = request.GET.get('folder', '')
    if folder_id and folder_id.isdigit():
        # parent_obj 获取到的不是一个 QuerySet 对象，而是单个 FileRepository 实例
        parent_obj = models.FileRepository.objects.filter(project=request.bugtracer.project, id=folder_id,
                                                          file_type=2).first()
    # 新建/编辑文件夹
    if request.method == 'POST':
        folderId = request.POST.get('folderId', '')

        # 如果有folderId，说明是编辑操作，否则是新建操作
        if folderId and folderId.isdecimal():
            folder_object = models.FileRepository.objects.filter(
                id=int(folderId),
                project=request.bugtracer.project,
                file_type=2
            ).first()
            form = FileModelForm(request, parent_obj, data=request.POST)
            if not folder_object:
                return JsonResponse({'status': False, 'error': form.errors})
        else:
            form = FileModelForm(request, parent_obj, data=request.POST)
            form.instance.project = request.bugtracer.project
            form.instance.file_type = 2
            form.instance.update_user = request.bugtracer.user
            form.instance.parent = parent_obj

        if form.is_valid():
            form.save()
            return JsonResponse({'status': True})
        else:
            return JsonResponse({'status': False, 'error': form.errors})
    else:
        form = FileModelForm(request, parent_obj, )

        # 获取当前目录下的文件列表（所有的文件夹和文件）
        queryset = models.FileRepository.objects.filter(project=request.bugtracer.project)
        if parent_obj:
            file_list = queryset.filter(parent=parent_obj).order_by('-file_type')
        else:
            file_list = queryset.filter(parent__isnull=True).order_by('-file_type')

        # 获取从根目录到当前目录的路径
        breadcrumb_list = []
        parent = parent_obj
        while parent:
            # 面包屑不仅要显示文件夹名称
            # 还需要能点击跳转到对应的文件夹
            # 跳转时需要文件夹的 ID 作为参数
            breadcrumb_list.insert(0, {'id': parent.id, 'name': parent.name})
            parent = parent.parent

        context = {
            'form': form,
            'breadcrumb_list': breadcrumb_list,
            'file_list': file_list,
            # 'folder_id': folder_id,
            # ... 其他上下文数据 ...
        }
        return render(request, 'web/file.html/', context)
