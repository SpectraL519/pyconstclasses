from itertools import product

import pytest
from constclasses.ccerror import ArgumentError, ConstError
from constclasses.const_class import const_class


class ConstClassBase:
    x: int
    s: str


ConstClass = const_class(ConstClassBase)


@const_class
class ConstClassDecorated:
    x: int
    s: str


test_classes = [ConstClass, ConstClassDecorated]

cls_args_combinations = [
    pytest.param(cls, args, id=f"cls={cls.__name__}, args={args}")
    for cls, args in product(test_classes, [(), (1,), (1, 2, 3)])
]


@pytest.mark.parametrize("const_cls, init_args", cls_args_combinations)
def test_const_class_initialization_with_invalid_number_of_arguments(
    const_cls, init_args: list
):
    with pytest.raises(ArgumentError) as err:
        _ = const_cls(init_args)

    err_msg = str(err.value)
    assert err_msg.startswith("Invalid number of arguments")


@pytest.mark.parametrize(
    "const_cls",
    [pytest.param(cls, id=f"cls={cls.__name__}") for cls in test_classes],
)
def test_const_class_member_modification(const_cls):
    x1, s1 = 1, "str1"
    x2, s2 = 2, "str2"

    const_instance = const_cls(x1, s1)

    with pytest.raises(ConstError) as err:
        const_instance.x = x2

    err_msg = str(err.value)
    assert err_msg == f"Cannot modify const attribute `x` of class `{const_cls.__name__}`"

    with pytest.raises(ConstError) as err:
        const_instance.s = s2

    err_msg = str(err.value)
    assert err_msg == f"Cannot modify const attribute `s` of class `{const_cls.__name__}`"
