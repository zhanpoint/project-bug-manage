from django import forms
from test import models
from django.core.validators import RegexValidator  # 正则验证类（第一个参数：正则表达式，第二个参数：格式错误提示内容）
from django.core.exceptions import ValidationError  # 验证错误信息


class RegisterModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 为每个字段添加对应样式
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': "请输入%s" % field.label})

    # 重写Register模型phone字段的验证规则
    phone = forms.CharField(label="手机号", validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])
    # 重写Register模型password字段，将password表单字段设置为密码输入框，确保用户输入的密码不会以明文形式显示在页面上。
    password = forms.CharField(label='密码', widget=forms.PasswordInput())

    # 添加字段
    confirm_password = forms.CharField(label='重复密码', widget=forms.PasswordInput())
    code = forms.CharField(label='验证码', widget=forms.TextInput())

    class Meta:
        model = models.UserInfo  # 指定需要关联的模型
        # fields = "__all__"  # 指定所有字段
        fields = ["username", "password", "confirm_password", "phone", "code"]  # 指定需要校验的字段及其顺序
