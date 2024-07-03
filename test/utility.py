import pytest


def assert_does_not_throw(func):
    try:
        func()
    except Exception as err:
        pytest.fail(f"Unexpected exception {type(err)}\nWhat:\n{err}")
