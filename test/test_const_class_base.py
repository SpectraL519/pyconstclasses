import test.common.utility as util

import pytest
from constclasses.ccerror import ConfigurationError
from constclasses.const_class_base import MANDATORY_CONST_ATTRS, ConstClassBase


def test_init_for_class_attrs_intersecting_with_mandatory_const_attrs():
    for attr_name in MANDATORY_CONST_ATTRS:
        with pytest.raises(ConfigurationError) as err:
            _ = ConstClassBase(cls_attrs={attr_name})
        assert util.config_not_empty_cls_attrs_intersection_msg_prefix() in util.msg(err)

    with pytest.raises(ConfigurationError) as err:
        _ = ConstClassBase(cls_attrs=MANDATORY_CONST_ATTRS)
    assert util.config_not_empty_cls_attrs_intersection_msg_prefix() in util.msg(err)


def test_init_for_not_none_include_and_exclude_parameters():
    with pytest.raises(ConfigurationError) as err:
        _ = ConstClassBase(include={}, exclude={})

    assert util.msg(err).endswith(
        util.config_include_and_exclude_used_error_msg_postfix()
    )


def test_init_for_exclude_intersecting_with_mandatory_const_fields():
    for mandatory_const_attr in MANDATORY_CONST_ATTRS:
        with pytest.raises(ConfigurationError) as err:
            _ = ConstClassBase(exclude={mandatory_const_attr})

        err_msg = str(err.value)
        assert err_msg.endswith(
            util.config_invalid_exclude_error_msg([mandatory_const_attr])
        )

    with pytest.raises(ConfigurationError) as err:
        _ = ConstClassBase(exclude=MANDATORY_CONST_ATTRS)

    err_msg = str(err.value)
    assert err_msg.endswith(util.config_invalid_exclude_error_msg(MANDATORY_CONST_ATTRS))


def test_init_with_valid_parameter_configuration():
    def _test():
        _ = ConstClassBase()

    util.assert_does_not_throw(_test)


@pytest.fixture
def gen_attributes():
    no_attrs = 8
    attrs = [f"attr{i+1}" for i in range(no_attrs)]
    return no_attrs, attrs


def test_is_const_attribute_with_default_include_and_exclude_parameters(gen_attributes):
    _, attrs = gen_attributes
    sut = ConstClassBase()

    for attr in MANDATORY_CONST_ATTRS | set(attrs):
        assert sut.is_const_attribute(attr)


def test_is_const_attribute_with_include_parameter(gen_attributes):
    no_attrs, attrs = gen_attributes
    include = attrs[: (no_attrs // 2)]
    sut = ConstClassBase(include=include)

    for attr in MANDATORY_CONST_ATTRS | set(include):
        assert sut.is_const_attribute(attr)

    for attr in attrs[(no_attrs // 2) :]:
        assert not sut.is_const_attribute(attr)


def test_is_const_attribute_with_exclude_parameter(gen_attributes):
    no_attrs, attrs = gen_attributes
    exclude = attrs[: (no_attrs // 2)]
    sut = ConstClassBase(exclude=exclude)

    for attr in exclude:
        assert not sut.is_const_attribute(attr)

    for attr in MANDATORY_CONST_ATTRS | set(attrs[(no_attrs // 2) :]):
        assert sut.is_const_attribute(attr)


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

    util.assert_does_not_throw(
        lambda: sut.process_attribute_type(attr_name, attr_type, BaseClass())
    )
    util.assert_does_not_throw(
        lambda: sut.process_attribute_type(attr_name, attr_type, DerivedClass())
    )

    with pytest.raises(TypeError):
        sut.process_attribute_type(attr_name, attr_type, NotDerivedClass())
