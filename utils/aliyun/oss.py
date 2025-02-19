import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
from itertools import islice
import os
import logging
import time
import random

from oss2.models import CorsRule, BucketCors

from Bug_manage.local_settings import alibaba_cloud_access_key_id, alibaba_cloud_access_key_secret

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 检查环境变量是否已设置
required_env_vars = ['OSS_ACCESS_KEY_ID', 'OSS_ACCESS_KEY_SECRET']
for var in required_env_vars:
    if var not in os.environ:
        logging.error(f"Environment variable {var} is not set.")
        exit(1)


def generate_unique_bucket_name():  # 生成唯一的Bucket名称
    # 获取当前时间戳
    timestamp = int(time.time())
    # 生成0到9999之间的随机数
    random_number = random.randint(0, 9999)
    # 将时间戳和随机数组合成唯一名称并返回
    bucket_name = f"demo-{timestamp}-{random_number}"
    return bucket_name


# 签名版本4要求请求中必须包含有效的区域信息region。
auth = oss2.ProviderAuthV4(EnvironmentVariableCredentialsProvider())
# endpoint 要与 region 对应
region = 'cn-wuhan-lr'  # 可选：关键字参数
endpoint = f'https://oss-{region}.aliyuncs.com'
# 生成唯一的Bucket名称
bucket_name = generate_unique_bucket_name()
# 初始化一个OSS（对象存储服务）的Bucket对象
bucket = oss2.Bucket(auth, endpoint, bucket_name, region=region)


def create_bucket(bucket_name, region):
    try:
        # 创建Bucket实例
        auth = oss2.Auth(alibaba_cloud_access_key_id, alibaba_cloud_access_key_secret)
        bucket = oss2.Bucket(auth, f'https://oss-{region}.aliyuncs.com', bucket_name)
        # 创建一个私有权限的存储桶
        bucket.create_bucket(oss2.models.BUCKET_ACL_PRIVATE)
        logging.info("Bucket created successfully")
    except oss2.exceptions.OssError as e:
        logging.error(f"Failed to create bucket: {e}")


def create_bucket_with_cors(bucket_name, region, allowed_origins=None, allowed_methods=None):
    """
    创建OSS桶并设置CORS规则

    Args:
        bucket_name (str): 桶名称
        allowed_origins (list): 允许的域名列表
        allowed_methods (list): 允许的HTTP方法列表
    """
    try:
        auth = oss2.Auth(alibaba_cloud_access_key_id, alibaba_cloud_access_key_secret)
        bucket = oss2.Bucket(auth, f'https://oss-{region}.aliyuncs.com', bucket_name)

        # 创建桶
        bucket.create_bucket(oss2.models.BUCKET_ACL_PRIVATE)

        # 设置默认值
        if allowed_origins is None:
            allowed_origins = ['*']
        if allowed_methods is None:
            # 阿里云OSS SDK在上传文件时自动使用了PUT方法，当上传文件时需要正确配置CORS设置包含PUT方法的规则
            allowed_methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD']

        # 创建CORS规则
        rule = CorsRule(
            allowed_origins=allowed_origins,
            allowed_methods=allowed_methods,
            allowed_headers=['*'],
            expose_headers=['ETag', 'x-oss-request-id'],
            max_age_seconds=86400
        )

        # 创建BucketCors对象并添加规则
        cors = BucketCors([rule])  # 关键修改：用列表包裹规则

        # 设置CORS规则
        bucket.put_bucket_cors(cors)  # 修改参数类型

        return {
            'status': 'success',
            'message': f'Bucket {bucket_name} created successfully with CORS rules'
        }

    except oss2.exceptions.ServerError as e:
        return {
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }

    except oss2.exceptions.ClientError as e:
        return {
            'status': 'error',
            'message': f'Client error: {str(e)}'
        }


def upload_file(bucket, key, data, headers=None):
    """
    :param bucket: 阿里云oss中指定的存储桶。
    :param key: 上传后在OSS中的对象名称（即文件路径和名称）
    :param data: 要上传的数据内容，可以是字符串、字节流或文件对象
    :return:
    """
    try:
        result = bucket.put_object(key, data)
        logging.info(f"File uploaded successfully, status code: {result.status}")
    except oss2.exceptions.OssError as e:
        logging.error(f"Failed to upload file: {e}")


def download_file(bucket, object_name):
    try:
        file_obj = bucket.get_object(object_name)
        content = file_obj.read().decode('utf-8')
        logging.info("File content:")
        logging.info(content)
        return content
    except oss2.exceptions.OssError as e:
        logging.error(f"Failed to download file: {e}")


def list_objects(bucket):
    try:
        objects = list(islice(oss2.ObjectIterator(bucket), 10))
        for obj in objects:
            logging.info(obj.key)
    except oss2.exceptions.OssError as e:
        logging.error(f"Failed to list objects: {e}")


# 删除桶中最多100个文件
def delete_objects(bucket):
    try:
        objects = list(islice(oss2.ObjectIterator(bucket), 100))
        if objects:
            for obj in objects:
                bucket.delete_object(obj.key)
                logging.info(f"Deleted object: {obj.key}")
        else:
            logging.info("No objects to delete")
    except oss2.exceptions.OssError as e:
        logging.error(f"Failed to delete objects: {e}")


# 删除桶
def delete_bucket(bucket_name, region):
    auth = oss2.Auth(
        alibaba_cloud_access_key_id,
        alibaba_cloud_access_key_secret
    )
    endpoint = f'http://oss-{region}.aliyuncs.com'

    try:
        # 删除存储桶及所有文件
        if bucket_name:
            bucket = oss2.Bucket(auth, endpoint, bucket_name)

            # 1. 删除所有对象
            for obj in oss2.ObjectIterator(bucket):
                bucket.delete_object(obj.key)

            # 2. 删除所有未完成的分片上传
            for upload in oss2.MultipartUploadIterator(bucket):
                bucket.abort_multipart_upload(upload.key, upload.upload_id)

            # 3. 删除存储桶本身
            bucket.delete_bucket()

    except oss2.exceptions.NoSuchBucket:
        pass  # 如果桶不存在则跳过
    # except Exception as e:
    #     return redirect(f'/web/setting/?error={str(e)}')


# 添加检查bucket是否存在
def check_bucket_exists(bucket):
    try:
        bucket.get_bucket_info()
        logging.info(f"Bucket {bucket.bucket_name} exists")
        return True
    except oss2.exceptions.NoSuchBucket:
        logging.error(f"Bucket {bucket.bucket_name} does not exist")
        return False
    except oss2.exceptions.OssError as e:
        logging.error(f"Failed to check bucket: {e}")
        return False


# 删除文件
def delete_file(bucket_name, key, region):
    """
    删除单个oss文件
    :param bucket_name: OSS bucket名称
    :param key: 文件key
    :param region: 区域
    :return:
    """
    auth = oss2.ProviderAuthV4(EnvironmentVariableCredentialsProvider())
    bucket = oss2.Bucket(auth, f'https://oss-{region}.aliyuncs.com', bucket_name, region=region)
    try:
        bucket.delete_object(key)
        logging.info(f"File {key} deleted successfully")
    except oss2.exceptions.OssError as e:
        logging.error(f"Failed to delete file: {e}")


# 删除多个文件
def delete_files(bucket_name, keys, region):
    """
    批量删除OSS文件
    :param bucket_name: OSS bucket名称
    :param keys: 文件key列表，最多支持1000个
    :param region: 区域
    """
    # 创建Bucket实例
    auth = oss2.Auth(alibaba_cloud_access_key_id, alibaba_cloud_access_key_secret)
    bucket = oss2.Bucket(auth, f'https://oss-{region}.aliyuncs.com', bucket_name)

    # 由于OSS限制每次最多删除1000个文件，所以需要分批处理
    chunk_size = 1000
    for i in range(0, len(keys), chunk_size):
        chunk_keys = keys[i:i + chunk_size]
        try:
            # 批量删除文件，quiet=True表示简单模式，不返回删除结果
            bucket.batch_delete_objects(chunk_keys)
        except oss2.exceptions.OssError as e:
            # 处理删除失败的情况
            print(f"删除文件失败: {str(e)}")
            raise e
