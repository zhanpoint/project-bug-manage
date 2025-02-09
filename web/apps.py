from django.apps import AppConfig


class WebConfig(AppConfig):
    # default_auto_field = 'django.db.models.AutoField'  # 覆盖全局配置（优先级更高）
    name = 'web'
