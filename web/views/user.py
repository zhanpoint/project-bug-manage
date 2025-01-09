from web.forms import sms_code
from django.http import JsonResponse
from django.shortcuts import render
from web.forms.register import RegisterModelForm


def register(request):
    if request.method == 'POST':
        form = RegisterModelForm(data=request.POST)
        if form.is_valid():
            # form.instance获取当前表单对应的模型实例, 然后调用save方法(会自动剔除Model中没有的字段)保存到数据库中
            form.instance.save()
            return JsonResponse({"status": True, 'url': 'https://www.baidu.com'})
        else:
            return JsonResponse({"status": False, 'error': form.errors})
    else:
        form = RegisterModelForm()
        return render(request, 'web/register.html', {'form': form})


# 将短信验证码的手机号和模版id的格式校验封装到sms_code.SmsCodeForm表单中1
def send_sms(request):
    # data是必填参数：表示用户提交的数据即request.POST 或 request.GET
    form = sms_code.SmsCodeForm(data=request.GET)
    # 表单校验通过
    if form.is_valid():
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, 'error': form.errors})
