from django.db import migrations
from django.db.models import F


def initialize_mptt_fields(apps, schema_editor):
    FileRepository = apps.get_model('web', 'FileRepository')

    # 初始化所有记录的 MPTT 字段
    for file_obj in FileRepository.objects.all():
        file_obj.lft = 1
        file_obj.rght = 2
        file_obj.tree_id = file_obj.id  # 使用 id 作为初始 tree_id
        file_obj.level = 0 if file_obj.parent_id is None else 1
        file_obj.save()


class Migration(migrations.Migration):
    dependencies = [
        ('web', '0012_filerepository_level_filerepository_lft_and_more'),  # 替换为你的上一个迁移文件名
    ]

    operations = [
        migrations.RunPython(initialize_mptt_fields),
    ]