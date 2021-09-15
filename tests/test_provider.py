import os
import unittest.mock
from typing import Type
from unittest import TestCase

import pytest

from storages.backends.amazon_s3 import AmazonS3Storage
from storages.backends.base import Storage
from storages.backends.file_system import FileSystemStorage
from storages.exceptions import MissingEnvironmentVariableError
from storages.provider import (DynamicStorageLoader,
                               EnvironmentVariablesCollector,
                               StorageConstructorArgumentsExtractor,
                               StorageProvider)


class TestStorageConstructorArgumentsExtractor(TestCase):
    class _TestStorage(Storage):
        def __init__(self, a, b, c, d, e):
            pass

    def test_extraction(self):
        arguments = StorageConstructorArgumentsExtractor.extract(
            storage_backend_class=self._TestStorage
        )
        expected_arguments = ("a", "b", "c", "d", "e")
        for index, argument in enumerate(arguments):
            assert argument == expected_arguments[index]

    def test_extraction_with_custom_ignored_arguments(self):
        arguments = StorageConstructorArgumentsExtractor.extract(
            storage_backend_class=self._TestStorage,
            ignored_arguments=("a", "b"),
        )
        expected_arguments = ("self", "c", "d", "e")
        for index, argument in enumerate(arguments):
            assert argument == expected_arguments[index]


class TestEnvironmentVariablesCollector:
    @pytest.fixture(autouse=True)
    def mock_environment(self):
        with unittest.mock.patch.dict(
            os.environ,
            {
                "STORAGES_PARAM_A": "a",
                "STORAGES_PARAM_B": "b",
                "STORAGES_PARAM_C": "c",
                "NOT_STORAGES_RELATED_PARAM": "any_value",
            },
        ):
            yield

    def test_collecting_a_and_b(self):
        names = ("param_a", "param_b")
        values = EnvironmentVariablesCollector.collect(names=names)
        assert values["param_a"] == "a"
        assert values["param_b"] == "b"
        assert len(values) == 2

    def test_collecting_b_and_c(self):
        names = ("param_b", "param_c")
        values = EnvironmentVariablesCollector.collect(names=names)
        assert values["param_b"] == "b"
        assert values["param_c"] == "c"
        assert len(values) == 2

    def test_collecting_prefixed(self):
        names = ("param",)
        values = EnvironmentVariablesCollector.collect(
            names=names, prefix="NOT_STORAGES_RELATED_"
        )
        assert values["param"] == "any_value"

    def test_missing_environment_variable(self):
        names = ("missing",)
        with pytest.raises(MissingEnvironmentVariableError):
            EnvironmentVariablesCollector.collect(names=names)


class TestDynamicStorageLoader(TestCase):
    _EXPECTED_RESULT = {
        "storages.backends.amazon_s3.AmazonS3Storage": AmazonS3Storage,
        "storages.backends.file_system.FileSystemStorage": FileSystemStorage,
    }

    def test_loader(self):
        for path, expected_class in self._EXPECTED_RESULT.items():
            loaded_class = DynamicStorageLoader.load_class(path)
            assert loaded_class is expected_class


class TestStorageProvider(TestCase):
    _EXPECTED_RESULT = {
        "storages.backends.amazon_s3.AmazonS3Storage": AmazonS3Storage,
        "storages.backends.file_system.FileSystemStorage": FileSystemStorage,
    }

    def test_provider(self):
        for path, expected_class in self._EXPECTED_RESULT.items():
            storage = StorageProvider.provide(backend_path=path)
            assert type(storage) == expected_class
