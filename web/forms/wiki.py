from web import models
from web.forms.bootstrap import BootstrapForm
from django import forms


class WikiModelForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = models.Wiki
        exclude = ('project', 'depth')  # 不要忘了要排除掉project和depth字段

    # 获取当前项目的所有wiki文档。
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # values_list传递一个或多个字段名作为参数，返回一个QuerySet，其中每个元素都是一个元组（默认情况下），包含所请求字段的值。
        # 查询当前项目的所有wiki文档的id和title。
        data = models.Wiki.objects.filter(project=request.bugtracer.project).values_list('id', 'title')
        # 修改表单字段father_id选项，如果当前项目有wiki文档，则可以选择其父文档id即可以在前端显示其可以选择的所有父文档。
        # 否则其可选择的父文档id为null即在起那段只能选择根目录。
        self.fields['father_id'].choices = [(None, '根目录')] + list(data)
