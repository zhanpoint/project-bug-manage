import json

import oss2
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from utils.aliyun import oss
from web.forms.wiki import WikiModelForm
from web.models import Wiki
import uuid


def wiki(request, project_id):
    if request.method == 'GET':
        wiki_id = request.GET.get('detail_id')
        if not wiki_id or not wiki_id.isdigit():  # 如果当前要查看的文档不存在或者格式不符合规范，则返回一个最初的wiki页面（右侧待新建的页面）
            return render(request, 'web/wiki.html/')
        else:  # 如果当前要查看的文档存在，则将该文档内容展示在右侧
            wiki_obj = Wiki.objects.filter(id=wiki_id, project_id=project_id).first()
            return render(request, 'web/wiki.html/', {'wiki_obj': wiki_obj})


def wiki_add(request, project_id):
    if request.method == 'POST':
        form = WikiModelForm(request, data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            if form.instance.father_id:  # 如果有父文档，则设置父文档的深度+1
                form.instance.depth += 1
            else:
                form.instance.depth = 0
            form.instance.project_id = project_id
            form.save()
            url = reverse('web:wiki', kwargs={'project_id': project_id})
            return redirect(url)
        else:
            return render(request, 'web/wiki_add.html/', {'form': form})
    else:
        form = WikiModelForm(request)
        # !!!:小bug1,添加项目时应该在wiki页面进行添加使用inclusion_tag,而不是新开一个页面浪费资源，提高代码复用度
        # !!!:小bug2,当为选中文档新建文档时其父文档必须是当前选中的文档的子文档或者根文档（当前文档）而不是所有wiki文档
        return render(request, 'web/wiki_add.html/', {'form': form})


def wiki_edit(request, project_id, wiki_id):
    wiki_obj = Wiki.objects.filter(id=wiki_id, project_id=project_id).first()
    if request.method == 'POST':
        form = WikiModelForm(request, data=request.POST, instance=wiki_obj)
        if form.is_valid():
            # 如果编辑了当前文档的父文档，则进行与创建文档时相同的条件处理
            if form.instance.father_id:  # 如果有父文档，则设置父文档的深度+1
                form.instance.depth += 1
            else:
                form.instance.depth = 0
            form.save()
            url = reverse('web:wiki', kwargs={'project_id': project_id})
            format_url = "{0}?wiki_detail={1}".format(url, wiki_id)
            # redirect 函数发送的是 GET 请求
            return redirect(format_url)
        else:  # 返回错误信息
            return render(request, 'web/wiki_add.html/', {'form': form})
    else:
        # 预填充表单：当创建表单时传递 instance 参数，表单会根据该实例的字段值自动填充表单字段，方便用户查看和修改
        # 保存修改：提交表单后，表单可以将用户输入的数据更新到这个实例，并保存到数据库中
        form = WikiModelForm(request, instance=wiki_obj)
        return render(request, 'web/wiki_add.html/', {'form': form})


def wiki_delete(request, project_id, wiki_id):
    if request.method == 'GET':
        # 当前项目的当前选中的wiki文档一定存在，否则不会显示编辑和删除按钮，所以直接删除即可不用判断是否存在
        Wiki.objects.filter(id=wiki_id, project_id=project_id).delete()
        url = reverse('web:wiki', kwargs={'project_id': project_id})
        return redirect(url)


def wiki_catalog(request, project_id):
    # json.load()进行反序列化解析 JSON 格式的字符串或文件，将它们转换为 Python 数据结构
    # 方式一：使用 serializers 模块中的 serialize 方法将 QuerySet 序列化为 JSON 字符串。
    # 方式二：将QuerySet转换为字典或元组的列表,然后使用json.dumps()进行序列化
    # 获取当前项目下的所有文档数据
    data = Wiki.objects.filter(project_id=project_id).values('id', 'title', 'father_id').order_by('depth', 'id')
    # JsonResponse内部调用Python的json.dumps()方法将传递的数据序列化为 JSON 字符串。
    return JsonResponse({'status': True, 'data': list(data)})


# 通常情况下，Django 会要求 POST 请求包含有效的 CSRF 令牌，以防止恶意网站发送请求。
# 使用 @csrf_exempt 装饰器后，该视图将不再检查 CSRF 令牌，适用于某些特殊情况或 API 接口
@csrf_exempt
def wiki_upload(request, project_id):
    # result 字典通常用在处理 Markdown 编辑器（如 Editor.md）的图片上传功能中，它是一个标准的响应格式：
    result = {
        'success': 0,  # 用于标识上传成功还是失败
        'message': None,  # 用于存储错误信息或成功提示
        'url': None  # 存储上传成功后的图片URL地址
    }
    if request.method == 'POST':
        file_obj = request.FILES.get('editormd-image-file')  # 获取markdown编辑器上传的图片文件对象
        if file_obj:
            try:
                # 生成文件名
                file_name = file_obj.name
                # key = f"{file_name}_{uuid.uuid4()}"
                key = f"{file_name}"

                # 上传文件到OSS
                bucket_name = f"bugtracer---{request.bugtracer.project.project_name}"
                bucket = oss2.Bucket(oss.auth, oss.endpoint, bucket_name, region=oss.region)
                if not oss.check_bucket_exists(bucket):
                    oss.create_bucket(bucket)

                oss.upload_file(bucket, key, file_obj)

                # 对于私有读写权限的OSS桶，直接使用URL是无法访问文件的。需要生成一个带签名的临时访问URL。
                # 使用bucket.sign_url()方法替代直接拼接URL,生成的URL会包含必要的认证信息，允许在有效期内访问私有文件
                # file_url = f"https://{bucket.bucket_name}.oss-cn-wuhan-lr.aliyuncs.com/{key}"
                file_url = bucket.sign_url('GET', key, 3600 * 7)

                # 更新返回结果
                result['success'] = 1
                result['url'] = file_url
                result['message'] = "上传成功"

            except Exception as e:
                result['message'] = f"上传失败：{str(e)}"
        else:
            result['message'] = '未检测到上传的文件'
    return JsonResponse(result)
