from django import template
from web.models import Comment

register = template.Library()


@register.inclusion_tag('inclusion_tag/comment_section.html')
def comment_sections(issue_obj):
    comments = Comment.objects.filter(issue=issue_obj).order_by('tree_id', 'lft')  # 获取指定问题的所有评论
    return {'comments': comments}


@register.filter
def multiply(value, arg):
    """自定义过滤器，用于计算缩进距离"""
    return value * arg
