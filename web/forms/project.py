from django import forms
from web.forms.bootstrap import BootstrapForm
from web.forms.widgets import ColorRadioSelect
from web.models import Project
from web import models


class NewProjectModelForm(BootstrapForm, forms.ModelForm):
    exclude_fields = ['project_color']

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    class Meta:
        model = Project
        fields = ['project_name', 'project_color', 'project_desc']
        # 由于project_desc字段是ChiarField类型,CharField 类型在 ModelForm 自动生成表单时，默认会生成一个 TextInput 类型的表单输入控件。
        # 由于TextInput是单行输入框有一个固定的宽度和高度，适合较短的文本输入，所以需要设置widget属性，否则无法显示textarea
        widgets = {
            'project_desc': forms.Textarea(attrs={'rows': 4, 'cols': 5}),
            # 用于在表单中提供一组互斥的单选按钮，用户只能选择其中一项
            'project_color': ColorRadioSelect(attrs={'class': 'color-radio'})
        }

    def clean_project_name(self):
        # 检验当前用户是否已经创建过同名项目
        project_name = self.cleaned_data['project_name']
        is_exist = models.Project.objects.filter(leader=self.request.bugtracer.user,
                                                 project_name=project_name).exists()
        if is_exist:
            raise forms.ValidationError('您已经创建过同名项目')
        number = models.Project.objects.filter(leader=self.request.bugtracer.user).count()
        rule_number = self.request.bugtracer.user.member_level.project_num
        if number >= rule_number:
            raise forms.ValidationError('您已创建了%s个项目，项目个数超限请升级套餐' % rule_number)
        return project_name
