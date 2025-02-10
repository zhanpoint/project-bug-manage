from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest
import json
import oss2
from Bug_manage import local_settings


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


def fetch_sts_token(access_key_id, access_key_secret, role_arn):
    """子用户角色扮演获取临时用户的密钥
        :param access_key_id: 子用户的 access key id
        :param access_key_secret: 子用户的 access key secret
        :param role_arn: STS角色的Arn
        :return StsToken: 临时凭证
    """
    # 创建ACS客户端：
    clt = client.AcsClient(
        access_key_id,  # 子用户AccessKeyId
        access_key_secret,  # 子用户AccessKeySecret
        'cn-wuhan-lr'  # 地域region
    )

    # 创建角色扮演请求
    req = AssumeRoleRequest.AssumeRoleRequest()
    req.set_accept_format('json')  # 设置返回格式为JSON
    req.set_RoleArn(role_arn)  # 设置要扮演的角色ARN
    req.set_RoleSessionName('oss-upload-session')  # 设置会话名称

    # 发送请求并获取响应
    body = clt.do_action_with_exception(req)  # 发送请求
    j = json.loads(oss2.to_unicode(body))  # 解析响应

    # 创建并填充STS Token对象
    token = StsToken()
    token.access_key_id = j['Credentials']['AccessKeyId']
    token.access_key_secret = j['Credentials']['AccessKeySecret']
    token.security_token = j['Credentials']['SecurityToken']
    token.request_id = j['RequestId']
    token.expiration = oss2.utils.to_unixtime(j['Credentials']['Expiration'], '%Y-%m-%dT%H:%M:%SZ')

    return token
