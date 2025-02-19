from django import forms
from django.utils import timezone

from web.models import Issue


class IssueModelForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'tags', 'description', 'status', 'priority', 'assignee', 'due_date']

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError('标题至少需要5个字符')
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) < 10:
            raise forms.ValidationError('问题描述至少需要10个字符')
        return description

    def clean(self):
        cleaned_data = super().clean()  # 继承父类的默认清洗逻辑，并自定义清洗逻辑
        status = cleaned_data.get('status')
        priority = cleaned_data.get('priority')
        due_date = cleaned_data.get('due_date')
        assignee = cleaned_data.get('assignee')

        if status == 'urgent' and not due_date:
            raise forms.ValidationError({
                'due_date': '紧急问题必须设置截止日期'
            })

        # if due_date and due_date < timezone.now().date():
        #     raise forms.ValidationError({
        #         'due_date': '截止日期不能早于今天'
        #     })

        if priority in ['high', 'critical'] and not assignee:
            raise forms.ValidationError({
                'assignee': '高优先级问题必须指派负责人'
            })

        return cleaned_data
