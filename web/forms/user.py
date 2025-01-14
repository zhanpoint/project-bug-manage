from django import forms
from web import models
from .bootstrap import BootstrapForm
from django.core.validators import RegexValidator  # 正则验证类（第一个参数：正则表达式，第二个参数：格式错误提示内容）
from django.core.exceptions import ValidationError  # 验证错误信息
from django.conf import settings
import random
from utils.aliyun import Sample
from utils.encrypt import sha_256
import redis


class SmsCodeForm(forms.Form):
    # 虽然在Ajax中可以对发送到服务器的手机号进行是否为空和格式验证，但是验证失败时，Ajax中不会返回错误信息，所以需要再这里进行验证
    phone = forms.CharField(label="手机号", validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])

    def clean_phone(self):  # 对通过phone字段钩子函数进行清洗
        # self.cleaned_data 是一个字典，包含所有通过验证的表单字段及其值。
        # !!!
        phone = self.cleaned_data.get('phone')

        # 2.判断该手机号是否存在与数据库中以及短信模版是否有问题
        is_exist = models.UserInfo.objects.filter(phone=phone).exists()

        tpl = self.data.get('tpl')
        templates_id = settings.ALIYUN_SMS_TEMPLATE.get(tpl)
        if not templates_id:
            raise ValidationError("短信模版不存在")
        else:
            if tpl == 'register' and is_exist:
                raise ValidationError("手机号已存在")
            if tpl == 'login' and not is_exist:
                raise ValidationError("手机号不存在")

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


class RegisterModelForm(BootstrapForm, forms.ModelForm):
    username = forms.CharField(label="用户名", validators=[RegexValidator(r'^[a-zA-Z0-9_-]{3,10}$', '用户名格式错误'), ])
    # 将password表单字段设置为密码输入框，确保用户输入的密码不会以明文形式显示在页面上。
    password = forms.CharField(label='密码', widget=forms.PasswordInput(),
                               validators=[RegexValidator(r'^[a-zA-Z0-9]{6,16}$', '密码格式错误'), ])
    # 重复密码字段不需要进行字段级别验证，只需要确保两次输入的密码一致即可。
    confirm_password = forms.CharField(label='重复密码', widget=forms.PasswordInput(), )
    phone = forms.CharField(label="手机号", validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])
    code = forms.CharField(label='验证码', widget=forms.TextInput(),
                           validators=[RegexValidator(r'^[0-9]{6}$', '验证码格式错误'), ])

    # 在 Meta 类中的 model 属性来指定ModelForm对应的模型类。
    class Meta:
        model = models.UserInfo
        # fields = "__all__"
        # 不允许member_level字段自动生成表单
        fields = ['username', 'password', 'confirm_password', 'phone', 'code']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if models.UserInfo.objects.filter(username=username).exists():
            raise ValidationError("用户名已存在，请选择其他用户名。")
        return username

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if models.UserInfo.objects.filter(phone=phone).exists():
            raise ValidationError("手机号已被注册，请填写其他手机号。")
        return phone

    def clean_code(self):
        cd = self.cleaned_data.get('code')
        ph = self.cleaned_data.get('phone')
        if not ph:  # 验证码是基于手机号的，手机号为空，则抛出异常不用再验证验证码
            raise ValidationError("")
        pool = redis.ConnectionPool(host='localhost', port=6379, password='333444', max_connections=100, )
        conn = redis.Redis(connection_pool=pool)
        redis_code = conn.get(ph)
        if not redis_code or redis_code.decode('utf-8') != cd.strip():  # 将 redis_code 从字节类型解码为字符串
            raise ValidationError("验证码错误，请重新输入。")
        return cd

    def clean(self):
        pw = self.cleaned_data.get('password')
        confirm_pw = self.cleaned_data.get('confirm_password')
        # 判断密码是否为空，如果为空，则抛出异常终止表单验证。否则将密码进行加密时会报错空字符串不能进行encode('utf-8')编码
        if not pw or not confirm_pw:
            raise ValidationError('')
        if pw != confirm_pw:
            self.add_error('confirm_password', "两次输入的密码不一致。")
        # 对验证通过的相同密码进行加密，重复密码无需加密因为其不再数据库中存储
        self.cleaned_data['password'] = sha_256(pw)
        return self.cleaned_data


class LoginSmsForm(BootstrapForm, forms.Form):
    phone = forms.CharField(label="手机号", validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])
    code = forms.CharField(label='验证码', widget=forms.TextInput(), )

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not models.UserInfo.objects.filter(phone=phone).exists():
            raise ValidationError('该手机号未被注册')
        else:
            return phone

    def clean_code(self):
        code = self.cleaned_data.get('code')
        phone = self.cleaned_data.get('phone')
        if not phone:  # 防止用户修改表单导致手机号为空，此时直接抛出错误不用再验证验证码了
            raise ValidationError("")

        pool = redis.ConnectionPool(host='localhost', port=6379, password='333444', max_connections=100, )
        conn = redis.Redis(connection_pool=pool)
        redis_code = conn.get(phone)
        if not redis_code or redis_code.decode('utf-8') != code.strip():  # 将 redis_code 从字节类型解码为字符串
            raise ValidationError("验证码错误，请重新输入。")
        return code


class LoginNameForm(BootstrapForm, forms.Form):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    username = forms.CharField(label='用户名',
                               validators=[RegexValidator(r'^[a-zA-Z0-9_-]{3,10}$', '用户名格式错误')],
                               error_messages={
                                   'required': '用户名不能为空'}
                               )
    # 传统表单提交时默认表单验证失败时会刷新页面，密码字段内容会被清空，其他字段内容保留，render_value=True使得在提交表单时即使验证失败，密码字段也不会被清空。
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(render_value=True),
                               validators=[RegexValidator(r'^[a-zA-Z0-9]{6,16}$', '密码格式错误'), ],
                               error_messages={
                                   'required': '密码不能为空'}
                               )
    code = forms.CharField(label='验证码',
                           validators=[RegexValidator(r'^[a-zA-Z]{6}$', '验证码格式错误'), ],
                           error_messages={
                               'required': '验证码不能为空'}
                           )

    def clean_code(self):
        code = self.cleaned_data.get('code')
        # 通过request.session可以获取到当前浏览器用户存储到session中的数据即session_data
        session_code = self.request.session.get('image_code')
        if not session_code:
            raise ValidationError('验证码已过期，请重新获取')
        # 验证码不区分大小写
        if code.strip().upper() != session_code.upper():
            raise ValidationError('验证码错误，请重新输入')
        return code

    def clean_password(self):
        pw = self.cleaned_data.get('password')
        # 对密码进行加密
        return sha_256(pw)
