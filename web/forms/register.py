from django import forms
from web import models
from django.core.validators import RegexValidator  # 正则验证类（第一个参数：正则表达式，第二个参数：格式错误提示内容）
from django.core.exceptions import ValidationError  # 接收表单字段验证失败时抛出的异常
import redis
from utils import encrypt


class RegisterModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 为每个字段添加对应样式
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': "请输入%s" % field.label})

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
        fields = ['username', 'password', 'confirm_password', 'phone', 'code']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if models.UserInfo.objects.filter(username=username).exists():
            raise ValidationError("用户名已存在，请选择其他用户名。")
        return username

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if models.UserInfo.objects.filter(phone=phone).exists():
            raise ValidationError("手机号已存在，请选择其他手机号。")
        return phone

    def clean_code(self):
        cd = self.cleaned_data.get('code')
        ph = self.cleaned_data.get('phone')
        pool = redis.ConnectionPool(host='localhost', port=6379, password='333444', max_connections=100, )
        conn = redis.Redis(connection_pool=pool)
        redis_code = conn.get(ph)
        if not redis_code:
            raise ValidationError("验证码已过期，请重新获取。")
        if redis_code.decode('utf-8') != cd.strip():  # 将 redis_code 从字节类型解码为字符串
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
        # 对验证通过的两次相同密码进行加密
        self.cleaned_data['password'] = encrypt.sha_256(pw)
        self.cleaned_data['confirm_password'] = encrypt.sha_256(confirm_pw)
        return self.cleaned_data
