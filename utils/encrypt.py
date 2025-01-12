import hashlib
import os
from django.conf import settings


def sha_256(password: str):
    # 使用SHA-256算法对密码进行哈希处理
    # 盐值通过在密码前或后添加一个随机的盐值来提高安全性。盐值可以防止彩虹表攻击，并确保即使两个用户使用相同的密码，生成的哈希值也会不同。

    # 生成一个随机的字节串作为盐值（这样做会使用户名密码登录时，密码校验始终不一致，因为即使是相同的密码由于盐是随机的即加密后的密码始终不同）
    # salt = os.urandom(16)
    # 使用固定的盐值
    # salt = b'settings.SECRET_KEY'

    salt = settings.SECRET_KEY.encode('utf-8')
    # 创建一个SHA-256哈希对象,并添加盐值
    sha256_hash = hashlib.sha256(salt)
    # 使用密码字节更新SHA-256哈希对象，生成加盐的哈希值
    sha256_hash.update(password.encode('utf-8'))
    # 将哈希对象转换为十六进制字符串并返回
    return sha256_hash.hexdigest()
