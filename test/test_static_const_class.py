import pytest
from constclasses.ccerror import ConstError, InitializationError
from constclasses.static_const_class import mutable_instance

from .common import S1, S2, S_ATTR_NAME, X1, X2, X_ATTR_NAME, StaticConstClass


def test_static_const_class_initialization_error():
    with pytest.raises(TypeError) as err:
        _ = StaticConstClass(X2, S2)

    err_msg = str(err.value)
    assert err_msg == "'StaticConstClass' object is not callable"


def test_static_const_class_member_modification():
    build_err_msg = (
        lambda member: f"Cannot modify const attribute `{member}` of class `StaticConstClass`"
    )

    with pytest.raises(ConstError) as err:
        StaticConstClass.x = X2

    err_msg = str(err.value)
    assert err_msg == build_err_msg(X_ATTR_NAME)

    with pytest.raises(ConstError) as err:
        StaticConstClass.s = S2

    err_msg = str(err.value)
    assert err_msg == build_err_msg(S_ATTR_NAME)


def test_mutable_instance_of_static_const_class():
    mut_instance = mutable_instance(StaticConstClass)

    assert mut_instance.x == X1
    assert mut_instance.s == S1

    mut_instance.x = X2
    assert mut_instance.x == X2

    mut_instance.s = S2
    assert mut_instance.s == S2
