import environment
from web import models


def create_issue_tags():
    # 预定义的标签
    tags = models.IssueTag.TAGS

    # 创建或更新标签
    for tag_key, _ in tags:  # 使用下划线忽略未使用的 tag_name
        tag, created = models.IssueTag.objects.get_or_create(name=tag_key)
        if created:
            print(f'已创建标签: {tag_key}')
        else:
            print(f'标签已存在: {tag_key}')


if __name__ == '__main__':
    print('开始创建问题标签...')
    create_issue_tags()
    print('问题标签创建完成！')
