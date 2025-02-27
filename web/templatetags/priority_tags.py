from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def priority_option(value, label, selected_value=None):
    label_class = {
        'critical': 'label-danger',
        'high': 'label-warning',
        'medium': 'label-info',
        'low': 'label-default',
    }.get(value, 'label-default')

    selected = 'selected' if value == selected_value else ''
    # 标准的HTML中<option>标签不支持子元素，浏览器可能会忽略其中的HTML标签，导致图标不显示
    # 需要使用支持选项内容自定义的插件，比如bootstrap-select，并确保其配置正确，比如使用data-content属性来包含HTML内容。
    html = f'''
        <option value="{value}" {selected} data-content="<span class='label {label_class}'>{label}</span> ">
            {label} 
        </option>
        '''
    return mark_safe(html)  # 标记一个字符串为安全的（即不会被自动转义）
