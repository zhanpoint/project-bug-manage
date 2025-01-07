import random
from Bug_manage import settings
from utils.aliyun import Sample
from django.shortcuts import render, HttpResponse
from test.forms.register import RegisterModelForm


def register(request):
    if request.method == 'POST':
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = RegisterModelForm()

    return render(request, 'test/templates/test/register.html', {'form': form})


def send_sms(request):
    # 从请求参数中获取模版id
    tpl = request.GET.get("tpl")
    template_id = settings.ALIYUN_SMS_TEMPLATE.get(tpl)
    # 如果找不到对应的模版ID，则返回“该模版不存在”的响应
    if not template_id:
        return HttpResponse("该模版不存在")
    code = random.randrange(100000, 999999)
    response = Sample.main('17837038625', template_id, "{'code': '%s'}" % code)
    if response.body.code == 'OK':
        return HttpResponse("成功发送短信")
    else:
        return HttpResponse("短信发送失败: " + response.body.message)
