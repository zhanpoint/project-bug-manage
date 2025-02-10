from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest
import json
import oss2
from Bug_manage import local_settings


class StsToken(object):
    """AssumeRole返回的临时用户密钥
        :param str access_key_id: 临时用户的access key id
        :param str access_key_secret: 临时用户的access key secret
        :param int expiration: 过期时间，UNIX时间，自1970年1月1日UTC零点的秒数
        :param str security_token: 临时用户Token
        :param str request_id: 请求ID
    """

    def __init__(self):
        self.access_key_id = ''
        self.access_key_secret = ''
        self.expiration = 0
        self.security_token = ''
        self.request_id = ''


def get_credential(access_key_id, access_key_secret, role_arn):
    """子用户角色扮演获取临时用户的密钥
        :param access_key_id: 子用户的 access key id
        :param access_key_secret: 子用户的 access key secret
        :param role_arn: STS角色的Arn
        :return StsToken: 临时凭证
    """
    clt = client.AcsClient(access_key_id, access_key_secret, 'cn-wuhan-lr')
    req = AssumeRoleRequest.AssumeRoleRequest()

    req.set_accept_format('json')
    req.set_RoleArn(role_arn)
    req.set_RoleSessionName('oss-upload-session')

    body = clt.do_action_with_exception(req)
    j = json.loads(oss2.to_unicode(body))
    token = StsToken()

    token.access_key_id = j['Credentials']['AccessKeyId']
    token.access_key_secret = j['Credentials']['AccessKeySecret']
    token.security_token = j['Credentials']['SecurityToken']
    token.request_id = j['RequestId']
    token.expiration = oss2.utils.to_unixtime(j['Credentials']['Expiration'], '%Y-%m-%dT%H:%M:%SZ')

    return token
    # ------------------------------------------------------
    # ACCESS_KEY_ID = local_settings.alibaba_cloud_access_key_id
    # ACCESS_KEY_SECRET = local_settings.alibaba_cloud_access_key_secret
    # ROLE_ARN = local_settings.ROLE_ARN
    #
    # # 创建AcsClient实例
    # clt = AcsClient(
    #     ACCESS_KEY_ID,
    #     ACCESS_KEY_SECRET,
    #     region
    # )
    #
    # # 创建并配置AssumeRole请求
    # request = AssumeRoleRequest()
    # request.set_RoleArn(ROLE_ARN)  # 设置角色ARN
    # request.set_RoleSessionName('oss-upload-session')  # 设置会话名称
    # request.set_DurationSeconds(3600)  # 凭证有效期1小时
    # request.set_accept_format('json')  # 设置返回数据格式
    #
    # # 发送请求
    # response = clt.do_action_with_exception(request)  # 发送AssumeRole请求以获取临时凭证的二进制响应
    # credentials = json.loads(response.decode('utf-8'))  # 将返回临时凭证根据指定编码规则解码为字符串，并解析为JSON格式
    #
    # return {
    #     'accessKeyId': credentials['Credentials']['AccessKeyId'],
    #     'accessKeySecret': credentials['Credentials']['AccessKeySecret'],
    #     'securityToken': credentials['Credentials']['SecurityToken'],
    #     'region': region,
    #     'endpoint': f'https://oss-{region}.aliyuncs.com',
    #     'bucket': bucket_name
    # }
