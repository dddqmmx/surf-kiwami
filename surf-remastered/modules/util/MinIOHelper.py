# -*- coding: utf-8 -*-
"""
Created By      : ZedFeorius
Created Time    : 2024/12/7 17:08
File Name       : MinIOHelper
Last Edit Time  : 2024/12/7 17:08
"""
from typing import List, Optional, Dict
from minio import Minio
from minio.error import S3Error
import os
import traceback

from surf.appsGlobal import get_logger

logger = get_logger('MinIO')


class MinIOHelper:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, endpoint: Optional[str] = None, access_key: Optional[str] = None, secret_key: Optional[str] = None, secure: bool = True):
        """
        初始化 MinIO 客户端，优先使用传入参数，否则从环境变量获取

        :param endpoint: MinIO 服务器的地址和端口，例如 'play.min.io:9000'
        :param access_key: 访问密钥
        :param secret_key: 秘密密钥
        :param secure: 是否使用 HTTPS
        """
        if self.__initialized:
            return
        endpoint = endpoint or os.getenv('MINIO_ENDPOINT', 'play.min.io:9000')
        access_key = access_key or os.getenv('MINIO_ACCESS_KEY', 'YOUR_ACCESS_KEY')
        secret_key = secret_key or os.getenv('MINIO_SECRET_KEY', 'YOUR_SECRET_KEY')
        secure = secure if secure is not None else os.getenv('MINIO_SECURE', 'True') == 'True'

        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        self.__initialized = True
        logger.info("MinIO 客户端初始化成功。")

    def create_bucket(self, bucket_name: str) -> bool:
        """
        创建存储桶，如果不存在则创建

        :param bucket_name: 存储桶名称
        :return: 成功返回 True，否则 False
        """
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
                logger.info(f"存储桶 '{bucket_name}' 创建成功。")
            else:
                logger.info(f"存储桶 '{bucket_name}' 已存在。")
            return True
        except S3Error as e:
            logger.error(f"创建存储桶失败: {e}\n{traceback.format_exc()}")
            return False

    def upload_file(self, bucket_name: str, object_name: str, file_path: str, content_type: str = 'application/octet-stream') -> bool:
        """
        上传文件到指定的存储桶

        :param bucket_name: 存储桶名称
        :param object_name: 文件名称（在存储桶中的路径）
        :param file_path: 本地文件路径
        :param content_type: 文件的内容类型
        :return: 成功返回 True，否则 False
        """
        try:
            result = self.client.fput_object(
                bucket_name=bucket_name,
                object_name=object_name,
                file_path=file_path,
                content_type=content_type
            )
            logger.info(f"文件 '{file_path}' 上传到 '{bucket_name}/{object_name}' 成功。ETag: {result.etag}")
            return True
        except S3Error as e:
            logger.error(f"上传文件失败: {e}\n{traceback.format_exc()}")
            return False

    def download_file(self, bucket_name: str, object_name: str, file_path: str) -> bool:
        """
        从指定的存储桶下载文件

        :param bucket_name: 存储桶名称
        :param object_name: 对象名称（在存储桶中的路径）
        :param file_path: 本地下载路径
        :return: 成功返回 True，否则 False
        """
        try:
            self.client.fget_object(
                bucket_name=bucket_name,
                object_name=object_name,
                file_path=file_path
            )
            logger.info(f"对象 '{bucket_name}/{object_name}' 下载到 '{file_path}' 成功。")
            return True
        except S3Error as e:
            logger.error(f"下载文件失败: {e}\n{traceback.format_exc()}")
            return False

    def delete_file(self, bucket_name: str, object_name: str) -> bool:
        """
        删除存储桶中的文件

        :param bucket_name: 存储桶名称
        :param object_name: 对象名称（在存储桶中的路径）
        :return: 成功返回 True，否则 False
        """
        try:
            self.client.remove_object(bucket_name=bucket_name, object_name=object_name)
            logger.info(f"对象 '{bucket_name}/{object_name}' 删除成功。")
            return True
        except S3Error as e:
            logger.error(f"删除文件失败: {e}\n{traceback.format_exc()}")
            return False

    def list_objects(self, bucket_name: str, prefix: str = "") -> List[str]:
        """
        列出存储桶中的所有对象

        :param bucket_name: 存储桶名称
        :param prefix: 对象前缀，用于筛选
        :return: 对象名称列表
        """
        try:
            objects = self.client.list_objects(bucket_name, prefix=prefix, recursive=True)
            object_list = [obj.object_name for obj in objects]
            logger.info(f"存储桶 '{bucket_name}' 中的对象列表: {object_list}")
            return object_list
        except S3Error as e:
            logger.error(f"列出对象失败: {e}\n{traceback.format_exc()}")
            return []

    def get_presigned_url(self, bucket_name: str, object_name: str, expiration: int = 3600) -> str:
        """
        获取对象的预签名 URL

        :param bucket_name: 存储桶名称
        :param object_name: 对象名称
        :param expiration: URL 有效期（秒）
        :return: 预签名 URL
        """
        try:
            url = self.client.presigned_get_object(bucket_name, object_name, expires=expiration)
            logger.info(f"获取预签名 URL 成功: {url}")
            return url
        except S3Error as e:
            logger.error(f"获取预签名 URL 失败: {e}\n{traceback.format_exc()}")
            return ""

    def get_presigned_put_url(self, bucket_name: str, object_name: str, expiration: int = 3600) -> str:
        """
        获取对象的预签名上传 URL

        :param bucket_name: 存储桶名称
        :param object_name: 对象名称
        :param expiration: URL 有效期（秒）
        :return: 预签名上传 URL
        """
        try:
            url = self.client.presigned_put_object(bucket_name, object_name, expires=expiration)
            logger.info(f"获取预签名上传 URL 成功: {url}")
            return url
        except S3Error as e:
            logger.error(f"获取预签名上传 URL 失败: {e}\n{traceback.format_exc()}")
            return ""

    def object_exists(self, bucket_name: str, object_name: str) -> bool:
        """
        检查对象是否存在于存储桶中

        :param bucket_name: 存储桶名称
        :param object_name: 对象名称
        :return: 存在返回 True，否则 False
        """
        try:
            self.client.stat_object(bucket_name, object_name)
            logger.info(f"对象 '{bucket_name}/{object_name}' 存在。")
            return True
        except S3Error as e:
            if e.code == "NoSuchKey":
                logger.info(f"对象 '{bucket_name}/{object_name}' 不存在。")
                return False
            logger.error(f"检查对象存在失败: {e}\n{traceback.format_exc()}")
            return False

    def get_object_metadata(self, bucket_name: str, object_name: str) -> Dict[str, any]:
        """
        获取对象的元数据

        :param bucket_name: 存储桶名称
        :param object_name: 对象名称
        :return: 对象元数据字典，如果失败返回空字典
        """
        try:
            stat = self.client.stat_object(bucket_name, object_name)
            metadata = {
                "etag": stat.etag,
                "size": stat.size,
                "content_type": stat.content_type,
                "last_modified": stat.last_modified
            }
            logger.info(f"获取对象元数据成功: {metadata}")
            return metadata
        except S3Error as e:
            logger.error(f"获取对象元数据失败: {e}\n{traceback.format_exc()}")
            return {}

    def copy_object(self, source_bucket: str, source_object: str, dest_bucket: str, dest_object: str) -> bool:
        """
        复制对象到另一个存储桶或相同存储桶的不同位置

        :param source_bucket: 源存储桶名称
        :param source_object: 源对象名称
        :param dest_bucket: 目标存储桶名称
        :param dest_object: 目标对象名称
        :return: 成功返回 True，否则 False
        """
        try:
            copy_source = f'/{source_bucket}/{source_object}'
            self.client.copy_object(dest_bucket, dest_object, copy_source)
            logger.info(f"对象 '{source_bucket}/{source_object}' 复制到 '{dest_bucket}/{dest_object}' 成功。")
            return True
        except S3Error as e:
            logger.error(f"复制对象失败: {e}\n{traceback.format_exc()}")
            return False
