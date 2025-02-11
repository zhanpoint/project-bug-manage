import json

from django.shortcuts import render
from web import models
from web.forms.file import FileModelForm
from django.http import JsonResponse
from utils.aliyun.oss import delete_file, delete_files
from django.db.models import Sum  # 从 Django 的数据库聚合函数模块中导入 Sum
import json
from utils.aliyun.sts import fetch_sts_token
from Bug_manage import local_settings
from mptt.managers import TreeManager


def file(request, project_id):
    """文件预览"""

    # 获取当前显示列表的父级文件夹对象
    parent_obj = None
    folder_id = request.GET.get('folder_id', '')
    if folder_id and folder_id.isdigit():
        # parent_obj 获取到的不是一个 QuerySet 对象，而是单个 FileRepository 实例
        parent_obj = models.FileRepository.objects.filter(project=request.bugtracer.project, id=folder_id,
                                                          file_type=2).first()
    if request.method == 'GET':
        form = FileModelForm(request, parent_obj, )

        # 获取当前目录下的文件列表（所有的文件夹和文件）
        queryset = models.FileRepository.objects.filter(project=request.bugtracer.project)
        if parent_obj:  # 非根目录
            file_list = queryset.filter(parent=parent_obj).order_by('-file_type')
        else:  # 根目录
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


def file_add(request, project_id):
    # 获取当前显示列表的父级文件夹对象
    parent_obj = None
    if request.method == 'POST':
        # 从POST数据中获取父文件夹ID
        parent_id = request.POST.get('parent', '')
        if parent_id and parent_id.isdigit():
            parent_obj = models.FileRepository.objects.filter(
                project=request.bugtracer.project,
                id=parent_id,
                file_type=2
            ).first()

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


def file_edit(request, project_id):
    if request.method == 'PUT':
        # 手动解析 PUT 请求体（也可以使用DRF中的APIView或GenericAPIView来处理PUT请求）
        try:
            data = json.loads(request.body)
            # 编辑按钮是在遍历已存在的文件夹时生成（folderID正常情况下一定不为空），除非有人恶意构造请求
            folderId = data.get('folderId', '')  # 当前操作文件夹id
            if folderId and folderId.isdecimal():
                folder_object = models.FileRepository.objects.filter(
                    id=int(folderId),
                    project=request.bugtracer.project,
                    file_type=2
                ).first()

                # 获取当前显示列表的父级文件夹对象
                parent_obj = folder_object.parent

                # 创建新的数据字典，只包含form需要的字段
                form_data = {
                    'name': data.get('name', '')  # 只传递name字段
                }

                # 在编辑操作时，添加了 instance=folder_object 参数，这样可以确保我们是在更新现有记录而不是创建新记录
                # parent_obj参数仍然是必须的，因为编辑操作需要查看该文件夹的父文件夹所有文件名以防止创建在同一目录下同名文件夹
                # 对于PUT请求中JSON格式的数据，不应该request.POST来获取数据，而是创建新的数据字典，只包含form需要的字段
                form = FileModelForm(request, parent_obj, data=form_data, instance=folder_object)
                if form.is_valid():
                    form.save()
                    return JsonResponse({'status': True})
                else:
                    return JsonResponse({'status': False, 'error': form.errors})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)


def file_delete(request, project_id):
    """删除文件夹/文件"""
    if request.method == 'POST':  # 最好使用delete请求
        folderId = request.POST.get('folderId')  # 操作的文件夹ID

        if not folderId or not folderId.isdecimal():
            return JsonResponse({'status': False, 'error': '参数错误'})

        folder_object = models.FileRepository.objects.filter(
            id=int(folderId),
            project=request.bugtracer.project,
        ).first()

        if not folder_object:
            return JsonResponse({'status': False, 'error': '文件或文件夹不存在'})

        if folder_object.file_type == 1:  # 删除文件
            # 更新项目剩余空间
            request.bugtracer.project.remain_space += folder_object.file_size  # 删除文件时，需要将文件大小加回剩余空间
            request.bugtracer.project.save()

            # 在阿里云oss删除文件
            delete_file(request.bugtracer.project.bucket_name, folder_object.key, request.bugtracer.project.region)

            # 在数据库中删除文件
            folder_object.delete()
            return JsonResponse({'status': True})
        else:  # 删除文件夹
            try:
                # 使用MPTT的get_descendants()方法获取所有子节点（包括文件和文件夹）
                descendants = folder_object.get_descendants()

                # 获取所有子文件（不包括文件夹）
                all_files = descendants.filter(file_type=1)

                # 计算所有文件的总大小
                # 对 file_size 字段进行求和，并将结果命名为 'total'，获取名为 'total' 的聚合结果， 如果结果为 None（没有文件时），则返回 0
                total_size = all_files.aggregate(total=Sum('file_size'))['total'] or 0

                # 获取所有文件的key
                file_keys = list(all_files.values_list('key', flat=True))

                if file_keys:
                    # 批量删除阿里云OSS文件
                    delete_files(
                        bucket_name=request.bugtracer.project.bucket_name,
                        keys=file_keys,
                        region=request.bugtracer.project.region
                    )

                    # 更新项目剩余空间
                    request.bugtracer.project.remain_space += total_size
                    request.bugtracer.project.save()

                # 删除文件夹（会级联删除所有子文件和子文件夹）
                folder_object.delete()
            except Exception as e:
                return JsonResponse({'status': False, 'error': f'删除文件夹失败：{str(e)}'})
            return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False, 'error': '请求方法错误'})


def file_bulk_upload(request, project_id):
    """批量保存文件记录"""
    if request.method == 'POST':
        try:
            # 检查项目剩余空间
            project = request.bugtracer.project
            total_size = sum(int(f['size']) for f in json.loads(request.POST.get('files'))) / 1024  # 将前端发送的字节转换为KB
            if project.remain_space < total_size:
                return JsonResponse({'status': False, 'error': '项目空间不足'})

            # 获取父文件夹
            parent_id = request.POST.get('parent', '')
            parent_obj = None
            if parent_id and parent_id.isdigit():
                parent_obj = models.FileRepository.objects.filter(
                    id=int(parent_id),
                    project=project,
                    file_type=2
                ).first()

            # 批量创建记录,并逐个保存已生成MPTT字段
            file_objs = [
                models.FileRepository(
                    name=f['name'],
                    file_type=1,
                    file_size=f['size'] / 1024,  # 将前端发送的字节转换为KB
                    key=f['key'],
                    file_extension=f['name'].split('.')[-1],
                    update_user=request.bugtracer.user,
                    project=project,
                    parent=parent_obj
                ).save() for f in json.loads(request.POST.get('files'))
            ]

            # 更新项目空间
            project.remain_space -= total_size
            project.save()

            return JsonResponse({'status': True})

        except Exception as e:
            return JsonResponse({'status': False, 'error': str(e)})

    return JsonResponse({'status': False, 'error': '无效请求'})


def file_credentials(request, project_id):
    """获取阿里云STS临时凭证，并返回"""
    try:
        project = request.bugtracer.project
        # 获取STS临时凭证
        sts_token = fetch_sts_token(
            local_settings.alibaba_cloud_access_key_id,
            local_settings.alibaba_cloud_access_key_secret,
            local_settings.alibaba_cloud_role_arn,
            duration_seconds=1800  # 设置临时凭证有效期为半小时（注意：如果本参数大于RAM角色最大会话时间会报错）
        )
        # 将STS Token对象转换为可序列化的字典
        credentials = {
            'accessKeyId': sts_token.access_key_id,
            'accessKeySecret': sts_token.access_key_secret,
            'securityToken': sts_token.security_token,
            'region': project.region,  # 从项目配置获取
            'bucket': project.bucket_name,  # 从项目配置获取
            # 'expiration': sts_token.expiration  # 前端SDK会自动处理令牌过期问题，不需要返回这个字段
        }
        return JsonResponse({
            'status': True,
            'data': credentials
        })
    except Exception as e:
        return JsonResponse({
            'status': False,
            'error': str(e)
        })
