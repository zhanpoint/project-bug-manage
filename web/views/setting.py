from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from web.models import Project
from utils.aliyun.oss import delete_bucket


def setting(request):
    # if not request.user.is_authenticated:
    #     return redirect('/web/login/name/')  # 确保用户已登录

    # 传递渲染setting模版时的上下文数据
    context = {
        'projects': Project.objects.filter(leader=request.bugtracer.user),  # 获取当前登录用户创建的所有项目
    }
    return render(request, 'web/setting.html', context)


@csrf_exempt
def myproject_delete(request, project_id):
    if request.method == 'POST':
        try:
            # 获取要删除的项目
            project = Project.objects.get(id=project_id)

            # 删除存储桶及所有文件
            # 确保阿里云账号有删除存储桶的权限（需要AliyunOSSFullAccess权限）
            delete_bucket(project.bucket_name, project.region)

            # 删除数据库记录
            project.delete()

            return JsonResponse({'status': True, 'message': '项目删除成功'})
        except Exception as e:
            return JsonResponse({'status': False, 'message': f'删除失败：{str(e)}'})
    else:
        return JsonResponse({'status': False, 'message': '请求方法不正确'})
