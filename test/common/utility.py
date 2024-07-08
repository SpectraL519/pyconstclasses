import pytest


def msg(err: Exception) -> str:
    return str(err.value)


def config_not_empty_cls_attrs_intersection_msg_prefix() -> str:
    return "Const class cannot have members"


def config_include_and_exclude_used_error_msg_postfix() -> str:
    return "`include` and `exclude` parameters cannot be used simultaneously"


def config_invalid_exclude_error_msg(attrs: list[str]) -> str:
    return f"attribute(s) [{', '.join(attrs)}] cannot be excluded"


def invalid_type_error_msg_prefix() -> str:
    return "Attribute value does not match the declared type"


def const_error_msg(member: str, cls_name) -> str:
    return f"Cannot modify const attribute `{member}` of class `{cls_name}`"


def assert_does_not_throw(func):
    try:
        func()
    except Exception as err:
        pytest.fail(f"Unexpected exception {type(err)}\nWhat:\n{err}")
