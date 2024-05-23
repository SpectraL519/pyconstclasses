from ..src.const_class import const_class

import pytest


def test_const_class():
    class TestClass:
        pass

    with pytest.raises(NotImplementedError):
        _ = const_class(TestClass)
