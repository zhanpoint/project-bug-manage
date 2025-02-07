import uuid

from django.db import models


# 用户表
class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=10)
    phone = models.CharField(verbose_name='手机号', max_length=11)
    # SHA-256加密后的密码哈希值长度为64个字符（十六进制表示），所以密码字段的长度最大为64
    password = models.CharField(verbose_name='密码', max_length=64)
    member_level = models.ForeignKey(verbose_name='会员等级', to='MemberLevel', on_delete=models.CASCADE, )


# 会员等级表
class MemberLevel(models.Model):
    category_choice = [(1, '普通用户'), (2, 'VIP会员'), (3, 'SVIP会员   ')]
    # choices属性用于定义字段的可选值。通常是一个包含元组的列表，每个元组的第一个元素是存储在数据库中的值，第二个元素是其对应的中文描述（普通用户、VIP会员、SVIP会员）
    category = models.SmallIntegerField(unique=True, verbose_name='会员等级', choices=category_choice, default=1)
    name = models.CharField(verbose_name='会员等级名称', max_length=10)
    # 价格字段值不能为负数
    price = models.DecimalField(verbose_name='价格', max_digits=10, decimal_places=2)
    project_num = models.PositiveIntegerField(verbose_name='支持创建的项目最大个数')
    project_member = models.PositiveIntegerField(verbose_name='支持项目成员最大个数')
    single_project_space = models.PositiveIntegerField(verbose_name='单项目空间大小最大值', help_text='单位为GB')
    single_file_space = models.PositiveIntegerField(verbose_name='单文件空间大小最大值', help_text='单位为MB')


# 交易记录表
class TransactionRecord(models.Model):
    # class Meta:  # 指定一个或多个字段名（以逗号分隔）。Django 将在默认排序时按顺序使用这些字段，以确定最新的记录。
    #     get_latest_by = 'id'
    status_choice = [(1, '未支付'), (2, '已支付'), (3, '处理中')]
    TRANSACTION_TYPES = [
        ('deposit', '存款'),
        ('withdrawal', '取款'),
        ('transfer', '转账'),
    ]
    # Django不会自动将非空且不唯一的字段设置为主键
    orderID = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=False)
    status = models.SmallIntegerField(verbose_name='交易状态', choices=status_choice)
    # 当用户表记录被删除时，所有关联的交易表记录也会被自动删除。反之，删除交易表记录不会影响用户表记录。
    user = models.ForeignKey(verbose_name='用户', to='UserInfo', on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name='交易金额', max_digits=10, decimal_places=2)
    # 当用户为普通用户时，默认其会员结束时间为None即无限期
    transaction_begin = models.DateTimeField(verbose_name='订单实际支付时间', null=True, blank=True)
    transaction_end = models.DateTimeField(verbose_name='会员实际结束时间', null=True, blank=True)
    # transaction_create = models.DateTimeField(verbose_name='订单创建时间', auto_now_add=True)


# 项目表
class Project(models.Model):
    color_choice = [(1, 'red'), (2, 'orange'), (3, 'yellow'), (4, 'green'), (5, 'blue'), (6, 'indigo'), (7, 'purple')]
    project_name = models.CharField(verbose_name='项目名称', max_length=10)
    # blank=True，则在表单提交时，该字段可以为空而不会引发验证错误
    project_desc = models.CharField(verbose_name='项目描述', max_length=100, null=True, blank=True)
    project_color = models.SmallIntegerField(verbose_name='项目颜色', choices=color_choice, default=1)
    remain_space = models.PositiveIntegerField(verbose_name='剩余空间', help_text='单位为kb')
    leader = models.ForeignKey(verbose_name='项目负责人', to='UserInfo', on_delete=models.CASCADE)
    join_number = models.PositiveIntegerField(verbose_name='项目成员数量', default=1)
    star = models.BooleanField(verbose_name='项目是否星标', default=False)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    bucket_name = models.CharField(verbose_name='项目对应的OSS存储桶', max_length=64, null=True, blank=True)
    region = models.CharField(verbose_name='项目所属区域', max_length=64, default='cn-wuhan-lr')

    # 只有当显式调用save()方法时，才会执行save方法并保存到数据库
    def save(self, *args, **kwargs):  # self 指的是当前的 Project 对象实例
        if not self.pk:  # 只在创建新项目时设置默认空间
            # 获取项目负责人的会员等级
            member_level = self.leader.member_level
            # 将单位从GB转换为MB (1GB = 1024MB)
            self.remain_space = member_level.single_project_space * 1024 * 1024
        # 调用 models.Model（Django模型的基类）的 save 方法
        super().save(*args, **kwargs)


# 项目成员表
class ProjectMember(models.Model):
    project = models.ForeignKey(verbose_name='项目', to='Project', on_delete=models.CASCADE)
    # inviter和member字段都指向同一个模型，默认情况下它们会生成相同的反向访问器名称即‘模型名称_set’，导致冲突
    # 可以通过related_name参数来指定不同的访问器名称
    member = models.ForeignKey(verbose_name='成员', to='UserInfo', on_delete=models.CASCADE, related_name='member')
    inviter = models.ForeignKey(verbose_name='邀请人', to='UserInfo', on_delete=models.CASCADE, related_name='inviter')
    star = models.BooleanField(verbose_name='该成员是否星标', default=False)
    member_join_time = models.DateTimeField(verbose_name='成员加入时间', auto_now_add=True)


# wiki项目文档表
class Wiki(models.Model):
    title = models.CharField(verbose_name='标题', max_length=16)
    content = models.TextField(verbose_name='内容', null=True, blank=True)
    project = models.ForeignKey(verbose_name='项目', to='Project', on_delete=models.CASCADE)
    # 在进行自关联时，Django会自动为该字段添加一个related_name属性，默认值为模型名称的小写加下划线_set。
    # 在进行自关联时，to属性可以为self或者当前模型名，表示自关联。
    # 如果一个模型的多个外键指向同一个模型，用related_name可以指定从被关联模型反向查询时使用的名称，避免反向关系名称冲突。
    # 由于使用了级联删除，当父文档被删除时，其子文档也会被删除。
    father_id = models.ForeignKey(verbose_name='父文档', to='self', on_delete=models.CASCADE, related_name='children',
                                  null=True, blank=True)
    # 由于当用户编辑文档时（例如修改当前<id值更小>的文档的父文档为<id值更大>的文档）可能会导致父文档由于id值更大而出现在当前修改文档的后面以至于
    # 当$("#id_" + item.father_id)而查找不到父文档id，因此需要添加深度字段，使文档数据能够按照层级关系进行排列，其次才是id值
    depth = models.PositiveIntegerField(verbose_name='文档层级', default=0)

    # __str__方法当输出或打印对象时通常返回一个描述对象状态的字符串。
    def __str__(self):
        return self.title


# 文件表
class FileRepository(models.Model):
    file_type_choices = [
        (1, '文件'),
        (2, '文件夹')
    ]

    name = models.CharField(verbose_name='名称', max_length=128)
    file_type = models.SmallIntegerField(verbose_name='文件类型', choices=file_type_choices)
    file_size = models.BigIntegerField(verbose_name='文件大小', help_text='单位为字节', null=True, blank=True)  # 文件夹大小为null
    file_path = models.CharField(verbose_name='文件路径', max_length=255, null=True, blank=True)
    key = models.CharField(verbose_name='OSS对象存储的key', max_length=128, null=True, blank=True)
    file_extension = models.CharField(verbose_name='文件后缀', max_length=32, null=True, blank=True)

    # 外键关联
    project = models.ForeignKey(verbose_name='所属项目', to='Project', on_delete=models.CASCADE)
    parent = models.ForeignKey(verbose_name='上级目录', to='self', null=True, blank=True,
                               related_name='children', on_delete=models.CASCADE)

    # 更新信息
    update_user = models.ForeignKey(verbose_name='最后更新者', to='UserInfo', on_delete=models.CASCADE)
    update_datetime = models.DateTimeField(verbose_name='最后更新时间', auto_now=True)

    class Meta:
        verbose_name = '文件库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
