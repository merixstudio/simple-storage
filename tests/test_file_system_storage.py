from datetime import datetime, timedelta
from unittest import TestCase

import pytest

from storages.backends.file_system import FileSystemStorage
from storages.exceptions import ImproperlyConfiguredError


class TestFileSystemStorage(TestCase):
    _TEST_FILE_NAME = "test_file.txt"
    _TEST_FILE_CONTENT = "Lorem ipsum dolor sit amet..."
    _TEST_FILE_CONTENT_BINARY = b"Binary lorem ipsum dolor sit amet..."

    @pytest.fixture(autouse=True)
    def init_storage(self, tmpdir):
        self._storage = FileSystemStorage(path=tmpdir)

    def test_improper_storage_initialization(self):
        with pytest.raises(ImproperlyConfiguredError):
            FileSystemStorage(path="")

    def test_file_not_exists(self):
        assert not self._storage.exists(self._TEST_FILE_NAME)

    def test_file_exists_upon_writing(self):
        self._write_contents_to_file()
        assert self._storage.exists(self._TEST_FILE_NAME)

    def test_file_contains_written_data(self):
        self._write_contents_to_file()
        assert (
            self._storage.read(self._TEST_FILE_NAME) == self._TEST_FILE_CONTENT
        )

    def test_file_contains_binary_written_data(self):
        self._write_contents_to_file(binary=True)
        assert (
            self._storage.read(self._TEST_FILE_NAME, mode="rb")
            == self._TEST_FILE_CONTENT_BINARY
        )

    def test_file_does_not_exist_upon_writing_and_deletion(self):
        self._write_contents_to_file()
        self._storage.delete(self._TEST_FILE_NAME)
        assert not self._storage.exists(self._TEST_FILE_NAME)

    def test_file_size_matches_content_size(self):
        self._write_contents_to_file()
        assert self._storage.size(self._TEST_FILE_NAME) == len(
            self._TEST_FILE_CONTENT
        )

    def test_file_creation_time(self):
        now = datetime.utcnow()
        self._write_contents_to_file()
        creation_time = self._storage.get_created_time(self._TEST_FILE_NAME)
        assert creation_time - now < timedelta(seconds=1)

    def test_file_modification_time(self):
        now = datetime.utcnow()
        self._write_contents_to_file()
        modification_time = self._storage.get_modified_time(
            self._TEST_FILE_NAME
        )
        assert modification_time - now < timedelta(seconds=1)

    def test_file_access_time(self):
        now = datetime.utcnow()
        self._write_contents_to_file()
        access_time = self._storage.get_access_time(self._TEST_FILE_NAME)
        assert access_time - now < timedelta(seconds=1)

    def _write_contents_to_file(self, binary: bool = False):
        self._storage.write(
            self._TEST_FILE_NAME,
            content=self._TEST_FILE_CONTENT_BINARY
            if binary
            else self._TEST_FILE_CONTENT,
            mode="xb" if binary else "x",
        )
