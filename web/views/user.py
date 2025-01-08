from web.forms import sms_code
from django.http import JsonResponse
from django.shortcuts import render
from web.forms.register import RegisterModelForm


def register(request):
    if request.method == 'POST':
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = RegisterModelForm()

    return render(request, 'web/register.html', {'form': form})


# 将短信验证码的手机号和模版id的格式校验封装到sms_code.SmsCodeForm表单中
def send_sms(request):
    # data是必填参数：表示用户提交的数据即request.POST 或 request.GET
    form = sms_code.SmsCodeForm(data=request.GET)
    # 表单校验通过
    if form.is_valid():
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, 'error': form.errors})
