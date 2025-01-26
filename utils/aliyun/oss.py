import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider

# 从环境变量中获取访问凭证。
auth = oss2.ProviderAuthV4(EnvironmentVariableCredentialsProvider())
# yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou-internal.aliyuncs.com。
endpoint = 'https://oss-cn-wuhan-lr-internal.aliyuncs.com'
# 填写Endpoint对应的Region信息，例如cn-hangzhou。
region = 'cn-wuhan-lr'

# 设置连接池的大小，默认值为10。
session = oss2.Session(pool_size=10)

# 填写Bucket名称。
bucket = oss2.Bucket(auth, endpoint, 'zhanpoint', region=region, connect_timeout=60, session=session)