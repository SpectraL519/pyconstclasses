import pytest
from constclasses.ccerror import ConstError, InitializationError
from constclasses.const_class import const_class
from constclasses.const_class_base import MANDATORY_CONST_ATTRS

import test.common.utility as util


X_ATTR_NAME = "x"
S_ATTR_NAME = "s"
ATTR_NAMES = {X_ATTR_NAME, S_ATTR_NAME}

ATTR_VALS_1 = {
    X_ATTR_NAME: 1,
    S_ATTR_NAME: "str1"
}
ATTR_VALS_2 = {
    X_ATTR_NAME: 2,
    S_ATTR_NAME: "str2"
}
DUMMY_VALUE = 3.14

@const_class
class ConstClass:
    x: int
    s: str


@pytest.mark.parametrize(
    "init_args",
    [pytest.param(args, id=f", args={args}") for args in [(), (1,), (1, 2, 3)]],
)
def test_const_class_initialization_with_invalid_number_of_arguments(init_args: list):
    with pytest.raises(InitializationError) as err:
        _ = ConstClass(init_args)
    assert util.msg(err).startswith("Invalid number of arguments")


def test_const_class_initialization_without_strict_types():
    @const_class(with_strict_types=False)
    class ConstClassNoStrictTypes:
        x: int
        s: str

    const_instance = None
    def _initialize_const_class_with_convertible_types():
        nonlocal const_instance
        const_instance = ConstClassNoStrictTypes(DUMMY_VALUE, DUMMY_VALUE)

    util.assert_does_not_throw(_initialize_const_class_with_convertible_types)
    assert const_instance.x == int(DUMMY_VALUE)
    assert const_instance.s == str(DUMMY_VALUE)


def test_const_class_initialization_with_strict_types():
    @const_class(with_strict_types=True)
    class ConstClassStrictTypes:
        x: int
        s: str

    with pytest.raises(TypeError) as err:
        _ = ConstClassStrictTypes(DUMMY_VALUE, ATTR_VALS_1[S_ATTR_NAME])
    assert util.msg(err).startswith(util.invalid_type_error_msg_prefix())

    with pytest.raises(TypeError) as err:
        _ = ConstClassStrictTypes(ATTR_VALS_1[X_ATTR_NAME], DUMMY_VALUE)
    assert util.msg(err).startswith(util.invalid_type_error_msg_prefix())


def test_const_class_member_modification():
    const_instance = ConstClass(*(ATTR_VALS_1.values()))

    for attr_name in ATTR_NAMES | MANDATORY_CONST_ATTRS:
        with pytest.raises(ConstError) as err:
            setattr(const_instance, attr_name, DUMMY_VALUE)
        assert util.msg(err) == util.const_error_msg(attr_name, ConstClass.__name__)


def test_const_class_member_modification_with_include_parameter():
    include = {X_ATTR_NAME}

    @const_class(include=include)
    class ConstClassInclude:
        x: int
        s: str

    const_instance = ConstClassInclude(*(ATTR_VALS_1.values()))

    # mandatory const attributes can never be modified
    for attr_name in MANDATORY_CONST_ATTRS | include:
        with pytest.raises(ConstError) as err:
            setattr(const_instance, attr_name, DUMMY_VALUE)
        assert util.msg(err) == util.const_error_msg(attr_name, ConstClassInclude.__name__)

    def _modify_not_const_memeber():
        const_instance.s = ATTR_VALS_2[S_ATTR_NAME]

    util.assert_does_not_throw(_modify_not_const_memeber)
    assert const_instance.s == ATTR_VALS_2[S_ATTR_NAME]


def test_const_class_member_modification_with_exclude_parameter():
    @const_class(exclude={X_ATTR_NAME})
    class ConstClassExclude:
        x: int
        s: str

    const_instance = ConstClassExclude(*(ATTR_VALS_1.values()))

    # mandatory const attributes can never be modified
    for attr_name in MANDATORY_CONST_ATTRS | {S_ATTR_NAME}:
        with pytest.raises(ConstError) as err:
            setattr(const_instance, attr_name, DUMMY_VALUE)
        assert util.msg(err) == util.const_error_msg(attr_name, ConstClassExclude.__name__)

    def _modify_not_const_memeber():
        const_instance.x = ATTR_VALS_2[X_ATTR_NAME]

    util.assert_does_not_throw(_modify_not_const_memeber)
    assert const_instance.x == ATTR_VALS_2[X_ATTR_NAME]
