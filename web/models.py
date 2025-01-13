from django.db import models


# 用户表
class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=10)
    phone = models.CharField(verbose_name='手机号', max_length=11)
    # SHA-256加密后的密码哈希值长度为64个字符（十六进制表示），所以密码字段的长度最大为64
    password = models.CharField(verbose_name='密码', max_length=64)


# 会员等级表
class MemberLevel(models.Model):
    category_choice = [(1, '普通用户'), (2, 'VIP会员'), (3, 'SVIP会员')]
    # choices属性用于定义字段的可选值。通常是一个包含元组的列表，每个元组的第一个元素是存储在数据库中的值，第二个元素是其对应的中文描述（普通用户、VIP会员、SVIP会员）
    category = models.SmallIntegerField(verbose_name='会员等级', choices=category_choice, default=1)
    name = models.CharField(verbose_name='会员等级名称', max_length=10)
    # 价格字段值不能为负数
    price = models.DecimalField(verbose_name='价格', max_digits=10, decimal_places=2)
    project_num = models.PositiveIntegerField(verbose_name='支持创建的项目最大个数')
    project_member = models.PositiveIntegerField(verbose_name='支持项目成员最大个数')
    single_project_space = models.PositiveIntegerField(verbose_name='单项目空间大小最大值', help_text='单位为GB')
    single_file_space = models.PositiveIntegerField(verbose_name='单文件空间大小最大值', help_text='单位为MB')


# 交易记录表
class TransactionRecord(models.Model):
    status_choice = [(1, '未支付'), (2, '已支付'), (3, '处理中')]
    TRANSACTION_TYPES = [
        ('deposit', '存款'),
        ('withdrawal', '取款'),
        ('transfer', '转账'),
    ]
    # UUIDField用于生成全局唯一的标识符,所以可作为主键使用
    transaction_id = models.UUIDField(primary_key=True)
    status = models.SmallIntegerField(verbose_name='交易状态', choices=status_choice)
    # 当用户表记录被删除时，所有关联的交易表记录也会被自动删除。反之，删除交易表记录不会影响用户表记录。
    user = models.ForeignKey(verbose_name='用户', to='UserInfo', on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name='交易金额', max_digits=10, decimal_places=2)
    # 当用户为普通用户时，默认其会员结束时间为None即无限期
    transaction_date = models.DateTimeField(verbose_name='交易开始时间', auto_now_add=True)
    transaction_deadline = models.DateTimeField(verbose_name='交易结束时间', null=True)


# 项目表
class Project(models.Model):
    color_choice = [(1, '红色'), (2, '橙色'), (3, '黄色'), (4, '绿色'), (5, '蓝色'), (6, '靛色'), (7, '紫色')]
    project_name = models.CharField(verbose_name='项目名称', max_length=10)
    # blank=True，则在表单提交时，该字段可以为空而不会引发验证错误
    project_desc = models.CharField(verbose_name='项目描述', max_length=100, null=True, blank=True)
    project_color = models.SmallIntegerField(verbose_name='项目颜色', choices=color_choice, default=1)
    remain_space = models.PositiveIntegerField(verbose_name='剩余空间', default=0, help_text='单位为MB')
    leader = models.ForeignKey(verbose_name='项目负责人', to='UserInfo', on_delete=models.CASCADE)
    join_number = models.PositiveIntegerField(verbose_name='项目成员数量', default=1)
    star = models.BooleanField(verbose_name='项目是否星标', default=False)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class ProjectMember(models.Model):
    project = models.ForeignKey(verbose_name='项目', to='Project', on_delete=models.CASCADE)
    # inviter和member字段都指向同一个模型，默认情况下它们会生成相同的反向访问器名称即‘模型名称_set’，导致冲突
    # 可以通过related_name参数来指定不同的访问器名称
    member = models.ForeignKey(verbose_name='成员', to='UserInfo', on_delete=models.CASCADE, related_name='member')
    inviter = models.ForeignKey(verbose_name='邀请人', to='UserInfo', on_delete=models.CASCADE, related_name='inviter')
    member_join_time = models.DateTimeField(verbose_name='成员加入时间', auto_now_add=True)


