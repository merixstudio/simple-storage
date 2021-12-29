from datetime import datetime
from typing import AnyStr, Optional

from google.cloud import storage

from storages.backends.base import Storage
from storages.exceptions import ImproperlyConfiguredError


class GoogleCloudStorage(Storage):
    _SERVICE_NAME = "google_cloud"

    def __init__(
        self,
        credentials_path: str,
        bucket_name: str,
    ):
        if not credentials_path:
            raise ImproperlyConfiguredError(
                name="credentials_path", value=credentials_path
            )
        if not bucket_name:
            raise ImproperlyConfiguredError(
                name="bucket_name", value=bucket_name
            )

        self._client = storage.Client.from_service_account_json(credentials_path)
        self._bucket_name = bucket_name
        self._bucket = self._client.get_bucket(self._bucket_name)

    def read(self, name: str, mode: str = "r") -> AnyStr:
        blob = self._bucket.blob(name)
        return blob.download_as_bytes() if "b" in mode else blob.download_as_string()

    def write(self, name: str, content: AnyStr, mode: str = "a"):
        self._bucket.blob(name).upload_from_string(content)

    def delete(self, name: str):
        self._bucket.blob(name).delete()

    def exists(self, name: str) -> bool:
        return self._bucket.blob.exists()

    def size(self, name: str) -> int:
        return self._bucket.get_blob(name).size

    def get_created_time(self, name: str) -> Optional[datetime]:
        blob = self._bucket.get_blob(name)
        return blob and blob.time_created

    def get_modified_time(self, name: str) -> Optional[datetime]:
        blob = self._bucket.get_blob(name)
        return blob and blob.updated

    def get_access_time(self, name: str) -> datetime:
        raise NotImplementedError(
            "Google Cloud Storage does not provide access time info."
        )
