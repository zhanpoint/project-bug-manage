from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .bootstrap import BootstrapForm
from .. import models


class FileModelForm(BootstrapForm, ModelForm):
    class Meta:
        model = models.FileRepository
        fields = ['name', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_name(self):
        # 获取用户提交的文件夹名称
        name = self.cleaned_data.get('name')
        # 获取当前表单对应的模型实例,从中获取父级目录和所属项目
        parent_object = self.instance.parent
        project = self.instance.project

        # 检查同级目录下是否存在重名文件夹
        exists = models.FileRepository.objects.filter(
            name=name,
            project=project,
            parent=parent_object,
            file_type=2
        ).exists()

        if exists:
            raise ValidationError('文件夹名称已存在')

        return name
