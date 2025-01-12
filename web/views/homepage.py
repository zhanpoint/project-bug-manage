from django.shortcuts import render, redirect


def index(request):
    return render(request, 'web/index.html')


def logout(request):
    # 清除当前用户的所有会话数据，确保用户完全退出系统。
    request.session.flush()
    return redirect('/web/index/')
