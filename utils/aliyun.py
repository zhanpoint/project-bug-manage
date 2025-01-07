from Bug_manage import settings

from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class Sample:
    def __init__(self):  # 创建类的实例时自动调用，用于初始化对象的状态
        pass

    @staticmethod
    def create_client() -> Dysmsapi20170525Client:
        config = open_api_models.Config(
            access_key_id=settings.ALIBABA_CLOUD_ACCESS_KEY_ID,
            access_key_secret=settings.ALIBABA_CLOUD_ACCESS_KEY_SECRET
        )
        # 返回客户端实例
        return Dysmsapi20170525Client(config)

    @staticmethod  # 短信发送的同步静态方法
    def main(
            phone: str,  # 接收人号码
            template_id: str,  # 模版ID
            template_dict: str  # 模版参数
    ) -> dysmsapi_20170525_models.SendSmsResponse:
        client = Sample.create_client()
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=phone,  # 接收人号码
            sign_name=settings.ALIYUN_SMS_SIGN2,  # 签名内容
            template_code=template_id,  # 模版ID
            template_param=template_dict  # 模版参数
        )
        try:
            response = client.send_sms_with_options(send_sms_request, util_models.RuntimeOptions())
        except Exception as error:
            # 错误 message
            print(str(error))
            # 诊断地址
            if hasattr(error, 'data') and isinstance(error.data, dict):
                print(error.data.get("Recommend"))
            UtilClient.assert_as_string(str(error))
            response = None

        return response
