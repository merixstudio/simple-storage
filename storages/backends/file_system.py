from datetime import datetime
from os import remove
from os.path import getatime, getctime, getmtime, getsize, join, lexists
from typing import AnyStr, Union

from storages.backends.base import Storage
from storages.exceptions import ImproperlyConfiguredError


class FileSystemStorage(Storage):
    def __init__(self, path: str):
        if not path:
            raise ImproperlyConfiguredError(name="path", value=path)
        self._base_path = path

    def _path(self, name: str) -> str:
        return join(self._base_path, name)

    @staticmethod
    def _date_from_timestamp(ts: Union[int, float]) -> datetime:
        return datetime.utcfromtimestamp(ts)

    def read(self, name: str, mode: str = "r") -> AnyStr:
        with open(file=self._path(name), mode=mode) as file:
            return file.read()

    def write(self, name: str, content: AnyStr, mode: str = "x"):
        with open(file=self._path(name), mode=mode) as file:
            file.write(content)

    def delete(self, name: str):
        remove(self._path(name))

    def exists(self, name: str) -> bool:
        return lexists(self._path(name))

    def size(self, name: str) -> int:
        return getsize(self._path(name))

    def get_created_time(self, name: str) -> datetime:
        return self._date_from_timestamp(getctime(self._path(name)))

    def get_modified_time(self, name: str) -> datetime:
        return self._date_from_timestamp(getmtime(self._path(name)))

    def get_access_time(self, name: str) -> datetime:
        return self._date_from_timestamp(getatime(self._path(name)))
