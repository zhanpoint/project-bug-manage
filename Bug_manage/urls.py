from django.conf.urls import include
from django.urls import re_path
from django.contrib import admin

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    # 旧版本错误写法
    # re_path(r'^web/', include('web.urls', namespace='web')),

    # 正确写法1：使用包含app_name的模块（需要应用内有app_name）
    re_path(r'^web/', include('web.urls')),

    # 正确写法2：显式传递元组
    # 当使用namespace时，include()的第一个参数要是(模块路径, app_name)元组
    # re_path(r'^web/', include(('web.urls', 'web'), namespace='web')),
    # 这里'my_custom_app_name=web'会覆盖应用内urls.py中的app_name（如果存在）
]
