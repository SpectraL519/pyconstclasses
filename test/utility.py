import pytest


def msg(err: Exception) -> str:
    return str(err.value)


def const_error_msg(member: str, cls_name) -> str:
    return f"Cannot modify const attribute `{member}` of class `{cls_name}`"


def assert_does_not_throw(func):
    try:
        func()
    except Exception as err:
        pytest.fail(f"Unexpected exception {type(err)}\nWhat:\n{err}")
