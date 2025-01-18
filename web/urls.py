from django.conf.urls import url, include  # url方法只使用django1版本，django2.2+使用path和re_path
from .views import user, homepage, project, projectmanage

urlpatterns = [
    # 用户认证相关
    url(r'^register/$', user.register, name='register'),  # 注册
    url(r'^login/sms/$', user.login_sms, name='login_sms'),  # 短信登录
    url(r'^login/name/$', user.login_name, name='login_name'),  # 用户名登录
    url(r'^imagecode/$', user.image_code, name='image_code'),  # 图片验证码
    url(r'^sms/$', user.send_sms, name='sms'),
    url(r'^index/$', homepage.index, name='index'),
    url(r'^logout/$', homepage.logout, name='logout'),

    # 项目相关
    url(r'^project/$', project.project, name='project'),
    # 匹配一个或多个单词字符，并将匹配到的内容命名为 project_type，命名捕获组需要用括号()括起来
    # url(r'^project/addstar/(?P<project_type>\w+)/?P<project_id>\d+/$', project.project_addstar,name='project_addstar')
    url(r'^project/addstar/$', project.project_addstar, name='project_addstar'),
    url(r'^project/cancelstar/$', project.project_cancelstar, name='project_cancelstar'),

    # 单项目管理功能相关（include第一项要用列表不能用元组）
    url(r'^projectmanage/(?P<project_id>\d+)/', include([
        url(r'^dashboard/$', projectmanage.dashboard, name='dashboard'),
        url(r'^issue/$', projectmanage.issue, name='issue'),
        url(r'^statistic/$', projectmanage.statistic, name='statistic'),
        url(r'^wiki/$', projectmanage.wiki, name='wiki'),
        url(r'^file/$', projectmanage.file, name='file'),
        url(r'^setting/$', projectmanage.setting, name='setting')
    ], None, None)),
]
