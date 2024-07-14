import test.common.utility as util

import pytest
from constclasses.ccerror import ConstError, InitializationError
from constclasses.const_class_base import MANDATORY_CONST_ATTRS
from constclasses.static_const_class import mutable_instance, static_const_class

X_ATTR_NAME = "x"
S_ATTR_NAME = "s"
ATTR_NAMES = {X_ATTR_NAME, S_ATTR_NAME}

ATTR_VALS_1 = {X_ATTR_NAME: 1, S_ATTR_NAME: "str1"}
ATTR_VALS_2 = {X_ATTR_NAME: 2, S_ATTR_NAME: "str2"}
DUMMY_VALUE = 3.14


@static_const_class
class StaticConstClass:
    x: int = ATTR_VALS_1[X_ATTR_NAME]
    s: str = ATTR_VALS_1[S_ATTR_NAME]


STATIC_CONST_CLASS_NAME = "StaticConstClass"


def test_initialization_error():
    with pytest.raises(TypeError) as err:
        _ = StaticConstClass(*(ATTR_VALS_2.values()))
    assert util.msg(err) == "'StaticConstClass' object is not callable"


def test_member_modification():
    for attr_name in ATTR_NAMES:
        with pytest.raises(ConstError) as err:
            setattr(StaticConstClass, attr_name, DUMMY_VALUE)
        assert util.msg(err) == util.const_error_msg(attr_name, STATIC_CONST_CLASS_NAME)


def test_member_modification_with_include_parameter():
    include = {X_ATTR_NAME}

    @static_const_class(include=include)
    class StaticConstClassInclude:
        x: int = ATTR_VALS_1[X_ATTR_NAME]
        s: str = ATTR_VALS_1[X_ATTR_NAME]

    # mandatory const attributes can never be modified
    for attr_name in MANDATORY_CONST_ATTRS | include:
        with pytest.raises(ConstError) as err:
            setattr(StaticConstClassInclude, attr_name, DUMMY_VALUE)
        assert util.msg(err) == util.const_error_msg(attr_name, "StaticConstClassInclude")

    def _modify_not_const_memeber():
        StaticConstClassInclude.s = ATTR_VALS_2[S_ATTR_NAME]

    util.assert_does_not_throw(_modify_not_const_memeber)
    assert StaticConstClassInclude.s == ATTR_VALS_2[S_ATTR_NAME]


def test_member_modification_with_exclude_parameter():
    @static_const_class(exclude={X_ATTR_NAME})
    class StaticConstClassExclude:
        x: int = ATTR_VALS_1[X_ATTR_NAME]
        s: str = ATTR_VALS_1[X_ATTR_NAME]

    # mandatory const attributes can never be modified
    for attr_name in MANDATORY_CONST_ATTRS | {S_ATTR_NAME}:
        with pytest.raises(ConstError) as err:
            setattr(StaticConstClassExclude, attr_name, DUMMY_VALUE)
        assert util.msg(err) == util.const_error_msg(attr_name, "StaticConstClassExclude")

    def _modify_not_const_memeber():
        StaticConstClassExclude.x = ATTR_VALS_2[X_ATTR_NAME]

    util.assert_does_not_throw(_modify_not_const_memeber)
    assert StaticConstClassExclude.x == ATTR_VALS_2[X_ATTR_NAME]


def test_initialization_without_strict_types():
    def _test():
        @static_const_class(with_strict_types=False)
        class StaticConstClassNoStrictTypes:
            x: int = DUMMY_VALUE
            s: str = DUMMY_VALUE

        assert StaticConstClassNoStrictTypes.x == int(DUMMY_VALUE)
        assert StaticConstClassNoStrictTypes.s == str(DUMMY_VALUE)

    util.assert_does_not_throw(_test)


def test_initialization_with_strict_types():
    def _test(x_value=ATTR_VALS_1[X_ATTR_NAME], s_value=ATTR_VALS_1[S_ATTR_NAME]):
        @static_const_class(with_strict_types=True)
        class StaticConstClassNoStrictTypes:
            x: int = x_value
            s: str = s_value

    with pytest.raises(TypeError) as err:
        _test(x_value=DUMMY_VALUE)
    assert util.msg(err).startswith(util.invalid_type_error_msg_prefix())

    with pytest.raises(TypeError) as err:
        _test(s_value=DUMMY_VALUE)
    assert util.msg(err).startswith(util.invalid_type_error_msg_prefix())


def test_member_modification_with_strict_types():
    """
    To test the with_strict_types parameter for member modification
    all members will be marked as not const.
    """

    @static_const_class(with_strict_types=True, exclude=ATTR_NAMES)
    class StaticConstClassStrictTypes:
        x: int = ATTR_VALS_1[X_ATTR_NAME]
        s: str = ATTR_VALS_1[S_ATTR_NAME]

    for attr_name in ATTR_NAMES:
        with pytest.raises(TypeError) as err:
            setattr(StaticConstClassStrictTypes, attr_name, DUMMY_VALUE)
        assert util.msg(err).startswith(util.invalid_type_error_msg_prefix())


def test_mutable_instance_of_static_const_class():
    mut_instance = mutable_instance(StaticConstClass)

    for attr_name in ATTR_NAMES:
        assert getattr(mut_instance, attr_name) == ATTR_VALS_1[attr_name]
        setattr(mut_instance, attr_name, ATTR_VALS_2[attr_name])
        assert getattr(mut_instance, attr_name) == ATTR_VALS_2[attr_name]

    for attr_name in MANDATORY_CONST_ATTRS:
        with pytest.raises(ConstError) as err:
            setattr(mut_instance, attr_name, DUMMY_VALUE)
        assert util.msg(err) == util.const_error_msg(
            "mutable_StaticConstClass", attr_name
        )
