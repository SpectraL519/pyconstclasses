import pytest
from constclasses.ccerror import ConfigurationError
from constclasses.const_class_base import MANDATORY_CONST_FIELDS, ConstClassBase

from .utility import assert_does_not_throw


def test_const_class_base_setup_for_not_none_include_and_exclude_parameters():
    with pytest.raises(ConfigurationError) as err:
        _ = ConstClassBase(include={""}, exclude={""})

    err_msg = str(err.value)
    assert err_msg.endswith(
        "`include` and `exclude` parameters cannot be used simultaneously"
    )


def test_const_class_base_setup_for_exclude_intersecting_with_mandatory_const_fields():
    build_err_msg = lambda attrs: f"attribute(s) [{', '.join(attrs)}] cannot be excluded"

    for mandatory_const_field in MANDATORY_CONST_FIELDS:
        with pytest.raises(ConfigurationError) as err:
            _ = ConstClassBase(exclude={mandatory_const_field})

        err_msg = str(err.value)
        assert err_msg.endswith(build_err_msg([mandatory_const_field]))

    with pytest.raises(ConfigurationError) as err:
        _ = ConstClassBase(exclude=MANDATORY_CONST_FIELDS)

    err_msg = str(err.value)
    assert err_msg.endswith(build_err_msg(MANDATORY_CONST_FIELDS))


def test_is_const_field_with_include_parameter():
    no_attrs = 8
    attrs = [f"attr{i+1}" for i in range(no_attrs)]

    include = attrs[: (no_attrs // 2)]
    sut = ConstClassBase(include=include)

    for attr in MANDATORY_CONST_FIELDS | set(include):
        assert sut.is_const_field(attr)

    for attr in attrs[(no_attrs // 2) :]:
        assert not sut.is_const_field(attr)


def test_is_const_field_with_exclude_parameter():
    no_attrs = 8
    attrs = [f"attr{i+1}" for i in range(no_attrs)]

    exclude = attrs[: (no_attrs // 2)]
    sut = ConstClassBase(exclude=exclude)

    for attr in exclude:
        assert not sut.is_const_field(attr)

    for attr in MANDATORY_CONST_FIELDS | set(attrs[(no_attrs // 2) :]):
        assert sut.is_const_field(attr)


def test_process_attribute_type_without_strict_types():
    """
    The process_attribute_type function should return a valid value
    for an attribute if the given values can be converted to the
    declared types.
    """

    sut = ConstClassBase(with_strict_types=False)

    attr_name = "x"
    attr_type = int
    attr_value_exact_type = 3
    attr_value_convertible_type = 3.14

    assert (
        sut.process_attribute_type(attr_name, attr_type, attr_value_exact_type)
        == attr_value_exact_type
    )
    assert sut.process_attribute_type(
        attr_name, attr_type, attr_value_convertible_type
    ) == attr_type(attr_value_convertible_type)


def test_process_attribute_type_with_strict_types():
    """
    The process_attribute_type functionshould return a valid value
    for an attribute only when the given value is an instance of
    the declared type. Otherwise it should throw an error.
    """

    sut = ConstClassBase(with_strict_types=True)

    class BaseClass:
        pass

    class DerivedClass(BaseClass):
        pass

    class NotDerivedClass:
        pass

    attr_name = "x"
    attr_type = BaseClass

    assert_does_not_throw(
        lambda: sut.process_attribute_type(attr_name, attr_type, BaseClass())
    )
    assert_does_not_throw(
        lambda: sut.process_attribute_type(attr_name, attr_type, DerivedClass())
    )

    with pytest.raises(TypeError):
        sut.process_attribute_type(attr_name, attr_type, NotDerivedClass())
