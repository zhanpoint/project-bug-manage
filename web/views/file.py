from django.shortcuts import render

from web import models
from web.forms.file import FileModelForm
from django.http import JsonResponse
from utils.aliyun.oss import delete_file


def file(request, project_id):
    """文件管理"""

    # 获取当前显示列表的父级文件夹对象
    parent_obj = None
    folder_id = request.GET.get('folder', '')
    if folder_id and folder_id.isdigit():
        # parent_obj 获取到的不是一个 QuerySet 对象，而是单个 FileRepository 实例
        parent_obj = models.FileRepository.objects.filter(project=request.bugtracer.project, id=folder_id,
                                                          file_type=2).first()
    # 新建/编辑/删除文件夹
    if request.method == 'POST':
        folderId = request.POST.get('folderId', '')  # 操作的文件夹 ID

        # 处理删除文件夹操作
        if request.POST.get('delete') == 'true':
            if not folderId or not folderId.isdecimal():
                return JsonResponse({'status': False, 'error': '参数错误'})

            folder_object = models.FileRepository.objects.filter(
                id=int(folderId),
                project=request.bugtracer.project,
            ).first()

            if folder_object.file_type == 1:  # 删除文件
                # 更新项目剩余空间
                request.bugtracer.project.remain_space += folder_object.file_size  # 删除文件时，需要将文件大小加回剩余空间
                request.bugtracer.project.save()

                # 在阿里云oss删除文件
                delete_file(request.bugtracer.project.bucket_name, folder_object.key, request.bugtracer.project.region)

                # 在数据库中删除文件
                folder_object.delete()
            else:  # 删除文件夹


            return JsonResponse({'status': True})

        # 如果有folderId，说明是编辑文件夹操作
        elif folderId and folderId.isdecimal():
            folder_object = models.FileRepository.objects.filter(
                id=int(folderId),
                project=request.bugtracer.project,
                file_type=2
            ).first()
            # 编辑按钮是在遍历已存在的文件夹时生成的，用户只能通过点击这些编辑按钮来触发编辑操作
            # 除非有人恶意构造请求，否则 ID 对应的文件夹必定存在，由于已经有了用户认证系统，Django 默认有 CSRF 保护，操作都在项目权限范围内,代码的安全性仍然是有保障的
            # if not folder_object:
            #     return JsonResponse({'status': False, 'error': '文件夹不存在'})

            # 在编辑操作时，添加了 instance=folder_object 参数，这样可以确保我们是在更新现有记录而不是创建新记录
            form = FileModelForm(request, parent_obj, data=request.POST, instance=folder_object)

        # 处理新建文件夹操作
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
