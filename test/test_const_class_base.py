import pytest
from constclasses.const_class_base import ConstClassBase
from .utility import assert_does_not_throw


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

    assert_does_not_throw(lambda: sut.process_attribute_type(attr_name, attr_type, BaseClass()))
    assert_does_not_throw(lambda: sut.process_attribute_type(attr_name, attr_type, DerivedClass()))

    with pytest.raises(TypeError):
        sut.process_attribute_type(attr_name, attr_type, NotDerivedClass())
