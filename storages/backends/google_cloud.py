import base64
import json
from datetime import datetime
from typing import AnyStr

from google.cloud import storage, exceptions  # type: ignore

from storages.backends.base import Storage
from storages.exceptions import ImproperlyConfiguredError


class GoogleCloudStorage(Storage):
    _SERVICE_NAME = "google_cloud"

    def __init__(
        self,
        google_cloud_credentials: str,
        google_cloud_bucket_name: str,
    ):
        if not google_cloud_credentials:
            raise ImproperlyConfiguredError(name="credentials_path")
        if not google_cloud_bucket_name:
            raise ImproperlyConfiguredError(name="google_cloud_bucket_name")

        self._client = storage.Client.from_service_account_info(
            json.loads(base64.b64decode(google_cloud_credentials))
        )
        self._bucket_name = google_cloud_bucket_name
        self._bucket = self._client.get_bucket(self._bucket_name)

    def _get_blob(self, name: str) -> storage.Blob:
        blob = self._bucket.get_blob(name)

        if blob is None:
            raise exceptions.NotFound(f"File {name} does not exist.")

        return blob

    def read(self, name: str, mode: str = "r") -> AnyStr:
        blob = self._bucket.blob(name)
        return blob.download_as_bytes()

    def write(self, name: str, content: AnyStr, mode: str = "a"):
        self._bucket.blob(name).upload_from_string(content)

    def delete(self, name: str):
        self._bucket.blob(name).delete()

    def exists(self, name: str) -> bool:
        return self._bucket.blob(name).exists()

    def size(self, name: str) -> int:
        return self._get_blob(name).size

    def get_created_time(self, name: str) -> datetime:
        return self._get_blob(name).time_created

    def get_modified_time(self, name: str) -> datetime:
        return self._get_blob(name).updated

    def get_access_time(self, name: str) -> datetime:
        raise NotImplementedError(
            "Google Cloud Storage does not provide access time info."
        )
