from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .bootstrap import BootstrapForm
from .. import models


class FileModelForm(BootstrapForm, ModelForm):
    class Meta:
        model = models.FileRepository
        fields = ['name', ]

    def __init__(self, request, parent_obj, is_file=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.parent = parent_obj
        self.is_file = is_file  # 新增参数标识是否是文件

    def clean_name(self):
        # 获取用户提交的文件夹/文件名称
        name = self.cleaned_data.get('name')

        # 根据类型设置查询条件
        file_type = 1 if self.is_file else 2

        # 构建查询集
        queryset = models.FileRepository.objects.filter(
            file_type=file_type,  # 动态设置文件类型
            name=name,
            project=self.request.bugtracer.project)

        # 编辑有两种情况，情况1：名称没改变，情况2：改成新名称）以上两种情况均成立
        # 针对情况1：如果当前实例已经存在（即有主键），则从查询集中排除当前实例，以避免重复操作
        if self.instance.pk:
            queryset = queryset.exclude(id=self.instance.pk)

        # 检查同级目录
        if self.parent:
            # 如果有父文件夹，检查同一父文件夹下是否存在同名文件夹
            exists = queryset.filter(parent=self.parent).exists()
        else:
            # 如果没有父文件夹（即根目录），检查根目录下是否存在同名文件夹
            # 字段名__查找类型=值
            exists = queryset.filter(parent__isnull=True).exists()

        if exists:
            error_msg = '文件名已存在' if self.is_file else '文件夹名称已存在'
            raise ValidationError(error_msg)

        return name
