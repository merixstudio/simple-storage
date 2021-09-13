import logging
from datetime import datetime
from os import environ
from tempfile import SpooledTemporaryFile
from typing import AnyStr

import boto3
from boto3 import Session
from boto3.resources.base import ServiceResource
from botocore.exceptions import ClientError
from botocore.response import StreamingBody

from storages.backends.base import Storage


class AmazonS3Storage(Storage):
    _SERVICE_NAME = "s3"

    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str, bucket_name: str):
        self._session: Session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        self._s3: ServiceResource = self._session.resource(
            service_name=self._SERVICE_NAME
        )
        self._bucket_name = bucket_name
        self._bucket = self._s3.Bucket(self._bucket_name)

    def _get_object(self, name: str) -> object:
        return self._bucket.Object(key=name)

    def read(self, name: str, mode: str = "r") -> AnyStr:
        body: StreamingBody = self._bucket.Object(key=name).get()["Body"]
        return body.read() if "b" in mode else body.read().decode("utf-8")

    def write(self, name: str, content: AnyStr, mode: str = "a"):
        self._bucket.put_object(Key=name, Body=content)

    def delete(self, name: str):
        self._bucket.Object(key=name).delete()

    def exists(self, name: str) -> bool:
        try:
            self._session.client(
                service_name=self._SERVICE_NAME
            ).head_object(Bucket=self._bucket_name, Key=name)
            return True
        except ClientError as cause:
            logging.info(cause, exc_info=True)
            return False

    def size(self, name: str) -> int:
        return self._get_object(name).content_length

    def get_created_time(self, name: str) -> datetime:
        raise NotImplementedError("S3 storage does not provide created time info.")

    def get_modified_time(self, name: str) -> datetime:
        return self._get_object(name).last_modified

    def get_access_time(self, name: str) -> datetime:
        raise NotImplementedError("S3 storage does not provide access time info.")


amazon_s3_storage = AmazonS3Storage(
    aws_access_key_id=environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=environ.get("AWS_SECRET_ACCESS_KEY"),
    bucket_name=environ.get("AWS_S3_BUCKET_NAME"),
)