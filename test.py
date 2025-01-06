from django_redis import get_redis_connection

conn = get_redis_connection("default")  # 这个default就是默认的指定ip和端口以及密码的Redis

# 设置键值以及超时时间ex(单位为秒)，值写入到Redis会自动转换为字符串，并最终转换为字节类型存储到Redis中
conn.set("key", "666", ex=30)

# 获取键值,如果存在获取到字节类型通过".encode()/.decode()"进行编码和解码，不存在则返回None
val = conn.get("key")
print(val.decode())
