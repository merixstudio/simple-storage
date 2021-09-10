from unittest import TestCase

import pytest

from storages.backends.amazon_s3 import amazon_s3_storage


class TestAWSS3Storage(TestCase):
    @pytest.fixture(autouse=True)
    def init_storage(self, tmpdir):
        self._storage = amazon_s3_storage

    def test_read(self):
        data = self._storage.read(name="test-coverage.png", mode="rb")
        print("xxx")
        print(data)
        print("xxx")
        assert False
