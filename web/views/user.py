from django.http import JsonResponse  # 一般发送Ajax请求时返回JSONResponse
from django.shortcuts import render, HttpResponse, redirect
from web.forms.user import RegisterModelForm, LoginNameForm, LoginSmsForm, SmsCodeForm
from web import models
from django.db.models import Q


def register(request):  # 用户注册
    if request.method == 'POST':
        form = RegisterModelForm(data=request.POST)
        if form.is_valid():
            # form.instance获取当前表单对应的模型实例, 然后调用save方法(会自动剔除Model中没有的字段)保存到数据库中
            form.instance.save()
            # 在 Django 中，URL 路径通常以斜杠 / 开头，表示这是一个绝对路径。如果缺少斜杠，Django 可能会将其视为相对路径
            # 在 Django 中，URL 路径通常以斜杠 / 结尾，表示这是一个目录路径。如果缺少斜杠，Django 可能会将其视为文件路径
            return JsonResponse({"status": True, 'url': '/web/login/name/'})
        else:
            return JsonResponse({"status": False, 'error': form.errors})
    else:
        form = RegisterModelForm()
        return render(request, 'web/register.html', {'form': form})


def login_sms(request):  # 短信登录
    if request.method == 'POST':
        form = LoginSmsForm(data=request.POST)
        if form.is_valid():
            # 登录成功，将该用户信息保存到session中，并重定向到首页
            user_obj = models.UserInfo.objects.filter(phone=form.cleaned_data.get('phone')).first()
            request.session['userinfo_id'] = user_obj.id
            return JsonResponse({"status": True, 'url': '/web/index/'})
        else:
            return JsonResponse({"status": False, 'error': form.errors})
    else:
        # 由于login不涉及数据库的操作，所以使用LoginSmsForm表单进行数据校验和展示即可
        form = LoginSmsForm()
        return render(request, 'web/login_sms.html', {'form': form})


def login_name(request):  # 用户名登录
    if request.method == 'POST':
        # request的请求头中存放着cookie信息，服务器通过cookie识别存放于session中用户信息，所以需要将request作为参数传入
        form = LoginNameForm(request, data=request.POST)
        if form.is_valid():
            # 此处只需校验用户名和密码是否存在即可
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # 在django的ORM中，Q可以用于构建复杂的查询条件，特别是当你需要进行“或”条件查询时
            user_obj = models.UserInfo.objects.filter(Q(username=username) | Q(phone=username)).first()
            if user_obj:
                # 登录成功，将用户名保存到session中，并重定向到首页
                request.session['userinfo_id'] = user_obj.id
                # 1.URL 字符串; 2.视图名称
                return redirect('/web/index/')
            else:
                form.add_error('username', '该用户名或密码不存在')
                return render(request, 'web/login_name.html', {'form': form})
        else:
            return render(request, 'web/login_name.html', {'form': form})
    else:
        form = LoginNameForm(request)
        return render(request, 'web/login_name.html', {'form': form})


# 将短信验证码中的手机号和模版的数据校验逻辑放在表单中可以提高代码的可维护性和可重用性，同时使使视图函数更加简洁，专注于业务逻辑。
def send_sms(request):
    # data是必填参数：表示原始提交的数据，未经过任何处理或验证
    form = SmsCodeForm(data=request.GET)
    # 表单校验通过
    if form.is_valid():
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, 'error': form.errors})


def image_code(request):
    from utils.picture_code import image_code
    from io import BytesIO
    image_object, code_str = image_code()
    # 将验证码字符串保存到session中(这里使用的是redis缓存作为存储引擎)
    request.session['image_code'] = code_str
    request.session.set_expiry(60)  # 设置session过期时间,默认是两周
    # 创建一个字节流缓冲区buffer
    buffer = BytesIO()
    # 将图像对象保存到缓冲区，格式为JPEG
    image_object.save(buffer, format='png')
    # 获取缓冲区中的字节数据(即显示的图片)
    image_data = buffer.getvalue()
    # 关闭缓冲区
    buffer.close()
    # 返回HttpResponse，设置内容类型为'image/jpeg'
    return HttpResponse(image_data)
