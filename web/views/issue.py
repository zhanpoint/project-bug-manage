from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from web.forms.issue import IssueModelForm
from django.core.paginator import Paginator
from web import models


def issue(request, project_id):
    # 获取项目
    project = models.Project.objects.get(id=project_id)
    if request.method == 'GET':
        form = IssueModelForm()

        # 获取所有用户
        users = models.UserInfo.objects.filter(
            # 项目负责人
            Q(id=project.leader.id) |
            # 项目成员
            Q(id__in=models.ProjectMember.objects.filter(project=project).values('member_id'))
        ).distinct()

        # 获取项目下的所有问题
        issues = models.Issue.objects.filter(project=project)

        # 分页处理
        paginator = Paginator(issues, 4)  # 创建分页器对象，设置每页显示4个问题
        page_number = request.GET.get('page')  # 获取请求中的页码参数
        page_obj = paginator.get_page(page_number)  # 根据页码获取对应页面的问题列表

        context = {
            'project_members': users,
            'form': form,
            'issues': page_obj,
            'page_obj': page_obj,
        }
        return render(request, 'web/issue.html', context)


def issue_create(request, project_id):
    if request.method == 'POST':
        tags = request.POST.getlist('tags')
        assignee = request.POST.getlist('assignee')

        form = IssueModelForm(data=request.POST, files=None)
        if form.is_valid():
            issue_obj = form.save(commit=False)
            issue_obj.creator = request.bugtracer.user
            issue_obj.project = models.Project.objects.get(id=project_id)
            issue_obj.save()

            # 明确处理tags和assignee字段
            if tags:
                tag_objects = models.IssueTag.objects.filter(id__in=tags)
                issue_obj.tags.set(tag_objects)  # 使用set()方法设置多对多关系

            if assignee:
                assignee_objects = models.UserInfo.objects.filter(id__in=assignee)
                issue_obj.assignee.set(assignee_objects)

            return JsonResponse({'status': True})
        # 表单验证失败
        return JsonResponse({'status': False, 'errors': form.errors})
    return JsonResponse({'status': False, 'message': '方法不允许'})


def issue_editor(request, project_id, issue_id):
    # 获取要编辑的问题
    issue_obj = get_object_or_404(models.Issue, id=issue_id, project_id=project_id)
    form = IssueModelForm(data=request.POST or None, instance=issue_obj)

    if request.method == 'POST':
        # 处理问题编辑表单提交
        tags = request.POST.getlist('tags')
        assignee = request.POST.getlist('assignee')

        if form.is_valid():
            issue_obj = form.save(commit=False)
            issue_obj.save()

            # 更新tags和assignee字段
            if tags:
                tag_objects = models.IssueTag.objects.filter(id__in=tags)
                issue_obj.tags.set(tag_objects)

            if assignee:
                assignee_objects = models.UserInfo.objects.filter(id__in=assignee)
                issue_obj.assignee.set(assignee_objects)

            return JsonResponse({'status': True})
        return JsonResponse({'status': False, 'errors': form.errors})
    else:
        context = {
            'issue_obj': issue_obj,
            'form': form,
        }
        return render(request, 'web/issue_editor.html', context)


def issue_comment(request, project_id, issue_id):
    issue_obj = get_object_or_404(models.Issue, id=issue_id, project_id=project_id)
    if request.method == 'POST':
        if request.POST.get('reaction_type'):
            return comment_reaction(request)
        else:
            """处理评论提交"""
            parent_id = request.POST.get('comment_parent')  # 获取父评论的ID
            content = request.POST.get('comment_content')  # 获取评论内容

            if not content:
                return JsonResponse({'status': False, 'message': '评论内容不能为空,请填写内容'})

            if len(content) > 1000:
                return JsonResponse({'status': False, 'message': '评论内容不能超过1000个字符'})

            try:
                # 如果有父评论ID，创建回复评论
                if parent_id:
                    parent_comment = models.Comment.objects.get(id=parent_id)
                    models.Comment.objects.create(
                        issue=issue_obj,
                        author=request.bugtracer.user,
                        content=content,
                        parent=parent_comment
                    )
                else:
                    # 创建顶级评论
                    models.Comment.objects.create(
                        issue=issue_obj,
                        author=request.bugtracer.user,
                        content=content
                    )
                return JsonResponse({'status': True, 'message': '评论发送成功'})
            except Exception as e:
                return JsonResponse({'status': False, 'message': str(e)})
    else:
        """获取更新后的评论HTML"""
        comments = models.Comment.objects.filter(issue=issue_obj)  # 获取指定问题的所有评论

        # 获取当前用户对每个评论的反应
        user_reactions = {}
        if request.bugtracer and request.bugtracer.user:  # 如果项目存在且项目用户已登录
            # 获取当前用户对每个评论的的反应
            reactions = models.UserCommentReaction.objects.filter(
                user=request.bugtracer.user,
                comment__in=comments
            )
            # 创建一个字典，键为评论ID，值为用户对评论的的反应类型
            user_reactions = {r.comment_id: r.reaction_type for r in reactions}

        comments_html = render_to_string('inclusion_tag/comment_section.html', {
            'comments': comments,
            'user_reactions': user_reactions
        })
        return JsonResponse({'status': True, 'html': comments_html})


def comment_reaction(request):
    comment_id = request.POST.get('comment_id')  # 获取评论ID
    comment = get_object_or_404(models.Comment, id=comment_id)  # 获取评论对象
    reaction_type = request.POST.get('reaction_type')  # 获取用户选择的反应类型

    # 原子操作
    with transaction.atomic():
        # 检查用户是否已经对此评论进行过反应
        existing = models.UserCommentReaction.objects.filter(
            user=request.bugtracer.user,
            comment=comment
        ).first()

        if existing:
            if existing.reaction_type == reaction_type:  # 如果用户之前已经对此评论进行过反应且反应类型与当前操作类型相同，则删除该反应
                # 减少comment表中对应的点赞/踩计数
                if reaction_type == 'like':
                    comment.like_count = models.F('like_count') - 1
                else:
                    comment.dislike_count = models.F('dislike_count') - 1
                comment.save()

                existing.delete()
                action = 'removed'
            else:  # 如果用户之前已经对此评论进行过反应且反应类型与当前操作类型不同，则更新反应类型
                # 如果是切换反应类型
                if existing.reaction_type == 'like':
                    # 从赞变踩
                    comment.like_count = models.F('like_count') - 1
                    comment.dislike_count = models.F('dislike_count') + 1
                else:
                    # 从踩变赞
                    comment.dislike_count = models.F('dislike_count') - 1
                    comment.like_count = models.F('like_count') + 1
                comment.save()

                existing.reaction_type = reaction_type
                existing.save()
                action = 'updated'
        else:
            # 新增反应
            if reaction_type == 'like':
                comment.like_count = models.F('like_count') + 1
            else:
                comment.dislike_count = models.F('dislike_count') + 1
            comment.save()

            models.UserCommentReaction.objects.create(
                user=request.bugtracer.user,
                comment=comment,
                reaction_type=reaction_type
            )
            action = 'added'

        # 使用 F() 表达式进行更新时，Django 实际上是直接在数据库层面执行更新操作，而不会自动更新 Python 对象中的值
        # 调用 refresh_from_db() 来从数据库重新加载数据，确保 Python 对象中的值与数据库同步
        comment.refresh_from_db()

    return JsonResponse({
        'status': True,
        'action': action,
        'like_count': comment.like_count,
        'dislike_count': comment.dislike_count,
        'user_reaction': reaction_type if action != 'removed' else None
    })


def issue_delete(request, project_id, issue_id):
    """删除问题"""
    if request.method == 'POST':
        try:
            # 获取要删除的问题对象
            issue_obj = models.Issue.objects.get(id=issue_id, project_id=project_id)
            # 删除问题
            issue_obj.delete()
            return JsonResponse({'status': True, 'message': '删除成功'})
        except models.Issue.DoesNotExist:
            return JsonResponse({'status': False, 'message': '问题不存在'})
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)})
    return JsonResponse({'status': False, 'message': '非法请求'})


def issue_search(request, project_id):
    """搜索问题"""
    search_term = request.GET.get('term', '').strip()  # 获取搜索关键词

    if not search_term:
        return JsonResponse({'status': False, 'message': '搜索关键词不能为空'})

    try:
        # 使用Q对象实现复杂查询，支持前缀、后缀和包含搜索
        # icontains: 不区分大小写的包含查询
        # istartswith: 不区分大小写的前缀查询
        # iendswith: 不区分大小写的后缀查询
        issues = models.Issue.objects.filter(
            project_id=project_id
        ).filter(
            Q(title__icontains=search_term) |  # 标题包含关键词
            Q(title__istartswith=search_term) |  # 标题以关键词开头
            Q(title__iendswith=search_term)  # 标题以关键词结尾
        ).select_related('creator').order_by('-updated_at')[:10]  # select_related('creator') 提前加载关联的创建者信息，减少数据库查询次数。

        # 构建搜索结果
        results = []
        for issue in issues:
            results.append({
                'id': issue.id,
                'title': issue.title,
                'status': issue.get_status_display(),
                'priority': issue.get_priority_display(),
                'creator': issue.creator.username,
                'updated_at': issue.updated_at.strftime('%Y-%m-%d'),
                'due_date': issue.due_date.strftime('%Y-%m-%d') if issue.due_date else '',
            })

        return JsonResponse({'status': True, 'data': results})
    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)})
