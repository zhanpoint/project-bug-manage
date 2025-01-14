import datetime

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from web import models
from django.conf import settings


class BugTracer(object):
    def __init__(self):
        self.user = None
        self.member_level = None
        self.project = None


class AllMiddleWare(MiddlewareMixin):
    # 当当前浏览器发生请求时，服务器通过请求头中的Cookie中随机字符串获取到用户信息（一条表记录），并查找该用户信息id字段值并返回查找到的这条记录obj
    # 然后在请求到达视图函数之前添加request.bugtracer，当视图函数处理请求时就可以通过request.bugtracer值判断该用户是否登录
    # 当然
    def process_request(self, request):
        request.bugtracer = BugTracer()

        # UserInfo中的id是自动生成的，userinfo_id从1开始，如果id为0表示该用户不存在即未登录
        obj = models.UserInfo.objects.filter(id=request.session.get('userinfo_id', 0)).first()
        request.bugtracer.user = obj  # 当前登录的用户
        if obj:  # (必须在用户注册以后才能执行)
            request.bugtracer.member_level = obj.member_level  # 获取当前登录用户的会员等级

        # 如果当前请求路径在白名单中，则不进行登录校验
        if request.path_info in settings.WEB_WHITE_LIST:
            return None

        # 否则如果用户未登录，则重定向到用户名密码登录页面
        if not obj:
            return redirect('/web/login/name/')

        """
        # 方式一:
        # 若该用户登录成功，则通过交易记录表获取该用户所拥有的最新交易记录的用户等级(前提是该用户必须已支付)
        
        latest_trade = models.TransactionRecord.objects.filter(user=obj, status=2).order_by('-id').first()
        # 如果该用户不是免费用户且该用户会员截止时间小于当前时间，则该用户会员已过期
        if latest_trade.transaction_end and latest_trade.transaction_end < datetime.datetime.now():
            # 当会员已过期时，获取该用户最开始的额度即该用户免费额度
            # latest_trade = models.TransactionRecord.objects.filter(user=obj, status=2).order_by('id').first()
            # 当一个模型通过外键关联到另一个模型时，可以使用双下划线来访问关联模型的字段
            latest_trade = models.TransactionRecord.objects.filter(user=obj, status=2, member_level__category=1).first()

        request.bugtracer.member_level = latest_trade.member_level
        """
        # 方式二:
        # latest() 可以接受一个或多个字段名作为参数，用于指定按哪个字段排序来确定“最新”的记录。
        latest_trade = models.TransactionRecord.objects.filter(user=obj, status=2).latest('id')
        if latest_trade.transaction_end and latest_trade.transaction_end < datetime.datetime.now():
            # 如果会员过期了将该用户会员等级重置为普通用户
            request.bugtracer.member_level = models.MemberLevel.objects.filter(category=1).first()
        # 如果是普通用户或会员用户且没有过期，则继续使用之前的会员等级，无需修改
