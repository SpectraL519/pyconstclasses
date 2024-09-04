import test.common.utility as util

import pytest
from constclasses.ccerror import ConstError, InitializationError
from constclasses.const_class import const_class
from constclasses.const_class_base import MANDATORY_CONST_ATTRS

X_ATTR_NAME = "x"
S_ATTR_NAME = "s"
ATTR_NAMES = {X_ATTR_NAME, S_ATTR_NAME}

ATTR_VALS_1 = {X_ATTR_NAME: 1, S_ATTR_NAME: "str1"}
ATTR_VALS_2 = {X_ATTR_NAME: 2, S_ATTR_NAME: "str2"}
DUMMY_VALUE = 3.14


@const_class
class ConstClass:
    x: int
    s: str


@pytest.mark.parametrize(
    "init_args",
    [pytest.param(args, id=f"args={args}") for args in [(), (1,), (1, 2, 3)]],
)
def test_initialization_with_invalid_number_of_arguments(init_args: list):
    with pytest.raises(InitializationError) as err:
        _ = ConstClass(init_args)
    assert util.msg(err).startswith("Invalid number of arguments")


def test_initialization_with_args():
    @const_class(with_kwargs=False)
    class ConstClassArgs:
        x: int
        s: str

    with pytest.raises(InitializationError):
        _ = ConstClassArgs()

    const_instance = None

    def _test_args():
        nonlocal const_instance
        const_instance = ConstClassArgs(*(ATTR_VALS_1.values()))

    util.assert_does_not_throw(_test_args)
    for attr_name, attr_value in ATTR_VALS_1.items():
        assert getattr(const_instance, attr_name) == attr_value


def test_initialization_with_kwargs():
    @const_class(with_kwargs=True)
    class ConstClassKwargs:
        x: int
        s: str

    with pytest.raises(TypeError):
        _ = ConstClassKwargs(*(ATTR_VALS_1.values()))

    const_instance = None

    def _test_kwargs():
        nonlocal const_instance
        const_instance = ConstClassKwargs(**ATTR_VALS_1)

    util.assert_does_not_throw(_test_kwargs)
    for attr_name, attr_value in ATTR_VALS_1.items():
        assert getattr(const_instance, attr_name) == attr_value


def test_member_modification():
    const_instance = ConstClass(*(ATTR_VALS_1.values()))

    for attr_name in ATTR_NAMES | MANDATORY_CONST_ATTRS:
        with pytest.raises(ConstError) as err:
            setattr(const_instance, attr_name, DUMMY_VALUE)
        assert util.msg(err) == util.const_error_msg(attr_name, ConstClass.__name__)


def test_member_modification_with_include_parameter():
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
        assert util.msg(err) == util.const_error_msg(
            attr_name, ConstClassInclude.__name__
        )

    def _modify_not_const_memeber():
        const_instance.s = ATTR_VALS_2[S_ATTR_NAME]

    util.assert_does_not_throw(_modify_not_const_memeber)
    assert const_instance.s == ATTR_VALS_2[S_ATTR_NAME]


def test_member_modification_with_exclude_parameter():
    @const_class(exclude={X_ATTR_NAME})
    class ConstClassExclude:
        x: int
        s: str

    const_instance = ConstClassExclude(*(ATTR_VALS_1.values()))

    # mandatory const attributes can never be modified
    for attr_name in MANDATORY_CONST_ATTRS | {S_ATTR_NAME}:
        with pytest.raises(ConstError) as err:
            setattr(const_instance, attr_name, DUMMY_VALUE)
        assert util.msg(err) == util.const_error_msg(
            attr_name, ConstClassExclude.__name__
        )

    def _modify_not_const_memeber():
        const_instance.x = ATTR_VALS_2[X_ATTR_NAME]

    util.assert_does_not_throw(_modify_not_const_memeber)
    assert const_instance.x == ATTR_VALS_2[X_ATTR_NAME]


def test_initialization_without_strict_types():
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


def test_initialization_with_strict_types():
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


def test_member_modification_with_strict_types():
    """
    To test the with_strict_types parameter for member modification
    all members will be marked as not const.
    """

    @const_class(with_strict_types=True, exclude=ATTR_NAMES)
    class ConstClassStrictTypes:
        x: int
        s: str

    const_instance = ConstClassStrictTypes(*(ATTR_VALS_1.values()))

    for attr_name in ATTR_NAMES:
        with pytest.raises(TypeError) as err:
            setattr(const_instance, attr_name, DUMMY_VALUE)
        assert util.msg(err).startswith(util.invalid_type_error_msg_prefix())


def test_initialization_with_inherited_constructor():
    @const_class(inherit_constructor=True)
    class ConstClassWithConstructor:
        x: int
        s: str

        def __init__(self, x: int):
            self.x = x
            self.s = str(x)

    x_value = ATTR_VALS_1[X_ATTR_NAME]
    const_instance = None

    def _initialize():
        nonlocal const_instance
        const_instance = ConstClassWithConstructor(x_value)

    util.assert_does_not_throw(_initialize)
    assert const_instance.x == x_value
    assert const_instance.s == str(x_value)


def test_new_with_kwargs():
    @const_class(with_kwargs=True)
    class ConstClassWithKwargs:
        x: int
        s: str

        def __eq__(self, other: object) -> bool:
            return (
                isinstance(other, self.__class__)
                and other.x == self.x
                and other.s == self.s
            )

    const_instance = ConstClassWithKwargs(**ATTR_VALS_1)

    # should create an exact copy by default
    const_instance_new_default = const_instance.new()
    assert const_instance_new_default == const_instance

    const_instance_new = const_instance.new(x=ATTR_VALS_2[X_ATTR_NAME])
    assert isinstance(const_instance_new, ConstClassWithKwargs)
    assert const_instance_new.s == const_instance.s
    assert const_instance_new.x == ATTR_VALS_2[X_ATTR_NAME]


def test_new_with_args():
    @const_class(with_kwargs=False)
    class ConstClassWithKwargs:
        x: int
        s: str

        def __eq__(self, other: object) -> bool:
            return (
                isinstance(other, self.__class__)
                and other.x == self.x
                and other.s == self.s
            )

    const_instance = ConstClassWithKwargs(*(ATTR_VALS_1.values()))

    # should create an exact copy by default
    const_instance_new_default = const_instance.new()
    assert const_instance_new_default == const_instance

    const_instance_new = const_instance.new(x=ATTR_VALS_2[X_ATTR_NAME])
    assert isinstance(const_instance_new, ConstClassWithKwargs)
    assert const_instance_new.s == const_instance.s
    assert const_instance_new.x == ATTR_VALS_2[X_ATTR_NAME]
