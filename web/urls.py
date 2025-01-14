from django.conf.urls import url  # url方法只使用django1版本，django2.2+使用path和re_path
from .views import user, homepage, project

urlpatterns = [
    # 用户认证相关
    url(r'^register/', user.register, name='register'),  # 注册
    url(r'^login/sms/', user.login_sms, name='login_sms'),  # 短信登录
    url(r'^login/name/', user.login_name, name='login_name'),  # 用户名登录
    url(r'^imagecode/', user.image_code, name='image_code'),  # 图片验证码
    url(r'^sms/', user.send_sms, name='sms'),
    url(r'^index/', homepage.index, name='index'),
    url(r'^logout/', homepage.logout, name='logout'),
    # 项目相关
    url(r'^project/', project.project, name='project'),
]
