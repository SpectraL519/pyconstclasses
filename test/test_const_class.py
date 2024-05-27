import pytest
from constclasses.ccerror import ConstError, InitializationError
from constclasses.const_class import const_class


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

    err_msg = str(err.value)
    assert err_msg.startswith("Invalid number of arguments")


def test_const_class_member_modification():
    x1, s1 = 1, "str1"
    x2, s2 = 2, "str2"

    const_instance = ConstClass(x1, s1)

    with pytest.raises(ConstError) as err:
        const_instance.x = x2

    build_err_msg = (
        lambda member: f"Cannot modify const attribute `{member}` of class `{ConstClass.__name__}`"
    )

    err_msg = str(err.value)
    assert err_msg == build_err_msg("x")

    with pytest.raises(ConstError) as err:
        const_instance.s = s2

    err_msg = str(err.value)
    assert err_msg == build_err_msg("s")
