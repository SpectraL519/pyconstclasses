import pytest
from constclasses.ccerror import ConstError, InitializationError

from .common import S1, S2, X1, X2, ConstClass, X_ATTR_NAME, S_ATTR_NAME


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
    build_err_msg = (
        lambda member: f"Cannot modify const attribute `{member}` of class `{ConstClass.__name__}`"
    )

    const_instance = ConstClass(X1, S1)

    with pytest.raises(ConstError) as err:
        const_instance.x = X2

    err_msg = str(err.value)
    assert err_msg == build_err_msg(X_ATTR_NAME)

    with pytest.raises(ConstError) as err:
        const_instance.s = S2

    err_msg = str(err.value)
    assert err_msg == build_err_msg(S_ATTR_NAME)
