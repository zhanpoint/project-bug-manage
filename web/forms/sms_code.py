from django import forms
from web import models
from django.core.validators import RegexValidator  # 正则验证类（第一个参数：正则表达式，第二个参数：格式错误提示内容）
from django.core.exceptions import ValidationError  # 验证错误信息
from django.conf import settings
import random
from utils.aliyun import Sample
import redis


class SmsCodeForm(forms.Form):
    # 虽然在Ajax中可以对发送到服务器的手机号进行是否为空和格式验证，但是验证失败时，Ajax中不会返回错误信息，所以需要再这里进行验证
    phone = forms.CharField(label="手机号", validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])

    def clean_phone(self):  # 对通过phone字段钩子函数进行清理和验证
        # self.cleaned_data 是一个字典，包含所有通过验证的表单字段及其值。
        phone = self.data.get('phone')

        # 2.判断该手机号是否存在与数据库中以及短信模版是否有问题
        is_exist = models.UserInfo.objects.filter(phone=phone).exists()
        tpl = self.data.get('tpl')
        templates_id = settings.ALIYUN_SMS_TEMPLATE.get(tpl)
        if not templates_id:
            raise ValidationError("短信模版错误")
        else:
            if tpl == 'login' and not is_exist:
                raise ValidationError("手机号不存在")
            elif tpl == 'register' and is_exist:
                raise ValidationError("手机号已存在")

        # 3.发送短信并验证短信是否发送成功
        code = random.randrange(100000, 999999)
        response = Sample.main(phone, templates_id, "{'code': '%s'}" % code)
        if response.body.code != 'OK' and response.body.message != 'OK':
            raise ValidationError("短信发送失败" + response.body.message)

        # 4.将接受到的短信写入到Redis缓存中中
        pool = redis.ConnectionPool(host='localhost', port=6379, password='333444', max_connections=100, )
        conn = redis.Redis(connection_pool=pool)
        conn.set(phone, code, ex=60)

        return phone
