from django.db import models


class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=10)
    phone = models.CharField(verbose_name='手机号', max_length=11)
    # SHA-256加密后的密码哈希值长度为64个字符（十六进制表示），所以密码字段的长度最大为64
    password = models.CharField(verbose_name='密码', max_length=64)
