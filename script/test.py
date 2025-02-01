import os

# 添加调试信息来查看所有环境变量
print("所有环境变量：", dict(os.environ))

# 具体检查OSS相关的环境变量
print("OSS_ACCESS_KEY_ID:", os.environ.get('OSS_ACCESS_KEY_ID'))
print("OSS_ACCESS_KEY_SECRET:", os.environ.get('OSS_ACCESS_KEY_SECRET'))