from unittest import TestCase

import pytest

from storages.backends.base import Storage


class TestAbstractStorage(TestCase):
    def test_initialization_raises_exception(self):
        with pytest.raises(TypeError):
            Storage()
