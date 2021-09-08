from abc import ABC, abstractmethod
from datetime import datetime
from typing import AnyStr


class Storage(ABC):
    @abstractmethod
    def read(self, name: str, mode: str = "r") -> AnyStr:
        pass  # pragma: no cover

    @abstractmethod
    def write(self, name: str, content: AnyStr, mode: str = "a"):
        pass  # pragma: no cover

    @abstractmethod
    def delete(self, name: str):
        pass  # pragma: no cover

    @abstractmethod
    def exists(self, name: str) -> bool:
        pass  # pragma: no cover

    @abstractmethod
    def size(self, name: str) -> int:
        """
        Returns size in bytes of the file specified by name.
        """
        pass  # pragma: no cover

    @abstractmethod
    def get_created_time(self, name: str) -> datetime:
        pass  # pragma: no cover

    @abstractmethod
    def get_modified_time(self, name: str) -> datetime:
        pass  # pragma: no cover

    @abstractmethod
    def get_access_time(self, name: str) -> datetime:
        pass  # pragma: no cover
