class BootstrapForm(object):  # 封装表单样式类，所有表单类均继承该类
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 为每个字段添加对应样式
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': "请输入%s" % field.label})
