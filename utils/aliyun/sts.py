from aliyunsdkcore.client import AcsClient
from aliyunsdksts.request.v20150401.AssumeRoleRequest import AssumeRoleRequest
import json
import oss2
from Bug_manage import local_settings


def get_credential(bucket_name, region):
    """获取STS临时凭证"""
    ACCESS_KEY_ID = local_settings.alibaba_cloud_access_key_id
    ACCESS_KEY_SECRET = local_settings.alibaba_cloud_access_key_secret
    ROLE_ARN = local_settings.ROLE_ARN

    # 创建AcsClient实例
    clt = AcsClient(
        ACCESS_KEY_ID,
        ACCESS_KEY_SECRET,
        region
    )

    # 创建并配置AssumeRole请求
    request = AssumeRoleRequest.AssumeRoleRequest()
    request.set_RoleArn(ROLE_ARN)  # 设置角色ARN
    request.set_RoleSessionName('oss-upload-session')  # 设置会话名称
    request.set_DurationSeconds(3600)  # 凭证有效期1小时
    request.set_accept_format('json')  # 设置返回数据格式

    # 发送请求
    response = clt.do_action_with_exception(request)  # 发送AssumeRole请求以获取临时凭证的二进制响应
    credentials = json.loads(response.decode('utf-8'))  # 将返回临时凭证根据指定编码规则解码为字符串，并解析为JSON格式

    return {
        'accessKeyId': credentials['Credentials']['AccessKeyId'],
        'accessKeySecret': credentials['Credentials']['AccessKeySecret'],
        'securityToken': credentials['Credentials']['SecurityToken'],
        'region': region,
        'bucket': bucket_name
    }
