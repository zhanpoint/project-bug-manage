# re_path方法只使用django1版本，django2.2+使用path和re_path,re_path() 完全等同于旧的 re_path()
from django.conf.urls import include
from django.urls import re_path
from .views import user, homepage, project, projectmenu, wiki, file

# 确保每个应用的urls.py中都定义了app_name
app_name = 'web'

urlpatterns = [
    # 用户认证相关
    re_path(r'^register/$', user.register, name='register'),  # 注册
    re_path(r'^login/sms/$', user.login_sms, name='login_sms'),  # 短信登录
    re_path(r'^login/name/$', user.login_name, name='login_name'),  # 用户名登录
    re_path(r'^imagecode/$', user.image_code, name='image_code'),  # 图片验证码
    re_path(r'^sms/$', user.send_sms, name='sms'),
    re_path(r'^index/$', homepage.index, name='index'),
    re_path(r'^logout/$', homepage.logout, name='logout'),

    # 项目相关
    re_path(r'^project/$', project.project, name='project'),
    # 匹配一个或多个单词字符，并将匹配到的内容命名为 project_type，命名捕获组需要用括号()括起来
    # re_path(r'^project/addstar/(?P<project_type>\w+)/?P<project_id>\d+/$', project.project_addstar,name='project_addstar')
    re_path(r'^project/addstar/$', project.project_addstar, name='project_addstar'),
    re_path(r'^project/cancelstar/$', project.project_cancelstar, name='project_cancelstar'),

    # 单项目管理功能相关（include第一项要用列表不能用元组）
    re_path(r'^projectmenu/(?P<project_id>\d+)/', include([
        re_path(r'^dashboard/$', projectmenu.dashboard, name='dashboard'),
        re_path(r'^issue/$', projectmenu.issue, name='issue'),
        re_path(r'^statistic/$', projectmenu.statistic, name='statistic'),
        # wiki相关功能
        re_path(r'^wiki/$', wiki.wiki, name='wiki'),
        re_path(r'^wiki/upload/$', wiki.wiki_upload, name='wiki_upload'),
        re_path(r'^wiki/add/$', wiki.wiki_add, name='wiki_add'),
        re_path(r'^wiki/edit/(?P<wiki_id>\d+)/$', wiki.wiki_edit, name='wiki_edit'),
        re_path(r'^wiki/delete/(?P<wiki_id>\d+)/$', wiki.wiki_delete, name='wiki_delete'),
        re_path(r'^wiki/cata_log/$', wiki.wiki_catalog, name='wiki_catalog'),
        # 文件相关功能
        re_path(r'^file/$', file.file, name='file'),
        re_path(r'^file/add/$', file.file_add, name='file_add'),
        re_path(r'^file/edit/$', file.file_edit, name='file_edit'),
        re_path(r'^file/delete/$', file.file_delete, name='file_delete'),
        re_path(r'^file/upload/$', file.file_upload, name='file_upload'),
        re_path(r'^file/bulk_upload/$', file.file_bulk_upload, name='file_bulk_upload'),
        # STS临时凭证
        re_path(r'^file/credentials/$', file.file_credentials, name='file_credentials'),
        # 项目设置功能
        re_path(r'^setting/$', projectmenu.setting, name='setting')
    ], None)),
]
