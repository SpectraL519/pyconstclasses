import pytest
from constclasses.ccerror import ConstError, InitializationError
from constclasses.const_class import const_class

from .common import S1, S2, S_ATTR_NAME, X1, X2, X_ATTR_NAME, ConstClass
from .utility import assert_does_not_throw, const_error_msg, msg


@pytest.mark.parametrize(
    "init_args",
    [pytest.param(args, id=f", args={args}") for args in [(), (1,), (1, 2, 3)]],
)
def test_const_class_initialization_with_invalid_number_of_arguments(init_args: list):
    with pytest.raises(InitializationError) as err:
        _ = ConstClass(init_args)
    assert msg(err).startswith("Invalid number of arguments")


def test_const_class_member_modification():
    const_instance = ConstClass(X1, S1)

    with pytest.raises(ConstError) as err:
        const_instance.x = X2
    assert msg(err) == const_error_msg(X_ATTR_NAME, ConstClass.__name__)

    with pytest.raises(ConstError) as err:
        const_instance.s = S2
    assert msg(err) == const_error_msg(S_ATTR_NAME, ConstClass.__name__)


def test_const_class_member_modification_with_include_parameter():
    @const_class(include={X_ATTR_NAME})
    class ConstClassInclude:
        x: int
        s: str

    const_instance = ConstClassInclude(X1, S1)

    with pytest.raises(ConstError) as err:
        const_instance.x = X2
    assert msg(err) == const_error_msg(X_ATTR_NAME, ConstClassInclude.__name__)

    def _modify_not_const_memeber():
        const_instance.s = S2

    assert_does_not_throw(_modify_not_const_memeber)
    assert const_instance.s == S2
