from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest
import json
import oss2
from Bug_manage import local_settings
import datetime
import time

""""""


class StsToken(object):
    """AssumeRole返回的临时用户密钥
        :param str access_key_id: 临时身份的访问密钥ID
        :param str access_key_secret: 临时身份的访问密钥密码
        :param int expiration: 凭证过期时间，UNIX时间，自1970年1月1日UTC零点的秒数
        :param str security_token: 临时安全令牌
        :param str request_id: 请求的唯一标识
    """

    def __init__(self):
        self.access_key_id = ''
        self.access_key_secret = ''
        self.expiration = 0
        self.security_token = ''
        self.request_id = ''


def fetch_sts_token(access_key_id, access_key_secret, role_arn, duration_seconds=3600):
    """子用户角色扮演获取临时用户的密钥
        子用户需要被授权AliyunSTSAssumeRoleAccess
        :param access_key_id: 子用户的 access key id
        :param access_key_secret: 子用户的 access key secret
        :param role_arn: STS角色的Arn
        :return StsToken: 临时凭证
    """
    # 参数校验（阿里云文档规定）
    if not 900 <= duration_seconds <= 43200:
        raise ValueError("有效期必须在900到43200秒之间（15分钟到12小时）")

    # 创建ACS客户端：
    clt = client.AcsClient(
        access_key_id,  # 子用户AccessKeyId
        access_key_secret,  # 子用户AccessKeySecret
        'cn-wuhan-lr'  # 地域region
    )

    # 创建角色扮演请求
    req = AssumeRoleRequest.AssumeRoleRequest()
    req.set_DurationSeconds(duration_seconds)  # 新增有效期设置
    req.set_accept_format('json')  # 设置返回格式为JSON
    req.set_RoleArn(role_arn)  # 设置要扮演的角色ARN
    req.set_RoleSessionName(f'oss-upload-{int(time.time())}')  # 设置会话名称:动态生成，加入时间戳或随机数，避免重复

    # 发送请求并获取响应
    try:  # 在请求处理部分添加异常处理
        body = clt.do_action_with_exception(req)
    except Exception as e:
        raise RuntimeError(f"STS请求失败: {str(e)}")
    j = json.loads(oss2.to_unicode(body))  # 解析响应

    # 创建并填充STS Token对象
    token = StsToken()
    token.access_key_id = j['Credentials']['AccessKeyId']
    token.access_key_secret = j['Credentials']['AccessKeySecret']
    token.security_token = j['Credentials']['SecurityToken']
    token.request_id = j['RequestId']
    # 处理时间转换（更推荐的方式）
    expiration_str = j['Credentials']['Expiration']  # 从返回的凭证信息中获取过期时间字符串（格式示例："2024-01-01T12:00:00Z"）
    token.expiration = int(datetime.datetime.strptime(  # 将字符串转换为datetime对象（UTC时区）
        expiration_str,
        '%Y-%m-%dT%H:%M:%SZ'  # # 匹配阿里云返回的时间格式
    ).timestamp())

    return token
