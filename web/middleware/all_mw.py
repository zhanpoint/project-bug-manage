from django.utils.deprecation import MiddlewareMixin
from web import models


class AllMiddleWare(MiddlewareMixin):
    # 当当前浏览器发生请求时，服务器通过请求头中的Cookie中随机字符串获取到用户信息（一条表记录），并查找该用户信息id字段值并返回查找到的这条记录obj
    # 然后在请求到达视图函数之前添加request.bugtracer，当视图函数处理请求时就可以通过request.bugtracer值判断该用户是否登录
    # 当然
    def process_request(self, request):
        # UserInfo中的id是自动生成的，userinfo_id从1开始，如果id为0表示该用户不存在即未登录
        obj = models.UserInfo.objects.filter(id=request.session.get('userinfo_id', 0)).first()
        request.bugtracer = obj
