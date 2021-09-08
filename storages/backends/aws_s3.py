from datetime import datetime
from typing import AnyStr

import boto3
from boto3.resources.base import ServiceResource

from storages.backends.base import Storage


class AmazonS3Storage(Storage):
    def __init__(self, s3: ServiceResource, bucket_name: str):
        self._bucket = s3.Bucket(bucket_name)

    def read(self, name: str, mode: str = "r") -> AnyStr:
        return self._bucket.Object(key=name)

    def write(self, name: str, content: AnyStr, mode: str = "a"):
        self._bucket.put_object(Body=content)

    def delete(self, name: str):
        pass

    def exists(self, name: str) -> bool:
        pass

    def size(self, name: str) -> int:
        pass

    def get_created_time(self, name: str) -> datetime:
        pass

    def get_modified_time(self, name: str) -> datetime:
        pass

    def get_access_time(self, name: str) -> datetime:
        pass


amazon_s3_storage = AmazonS3Storage(s3=boto3.resource("s3"), bucket_name="default")
