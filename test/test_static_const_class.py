import pytest
from constclasses.ccerror import ConstError, InitializationError
from constclasses.static_const_class import mutable_instance

from .common import (
    S1,
    S2,
    S_ATTR_NAME,
    STATIC_CONST_CLASS_NAME,
    X1,
    X2,
    X_ATTR_NAME,
    StaticConstClass,
)
from .utility import const_error_msg, msg


def test_static_const_class_initialization_error():
    with pytest.raises(TypeError) as err:
        _ = StaticConstClass(X2, S2)
    assert msg(err) == "'StaticConstClass' object is not callable"


def test_static_const_class_member_modification():
    with pytest.raises(ConstError) as err:
        StaticConstClass.x = X2
    assert msg(err) == const_error_msg(X_ATTR_NAME, STATIC_CONST_CLASS_NAME)

    with pytest.raises(ConstError) as err:
        StaticConstClass.s = S2
    assert msg(err) == const_error_msg(S_ATTR_NAME, STATIC_CONST_CLASS_NAME)


def test_mutable_instance_of_static_const_class():
    mut_instance = mutable_instance(StaticConstClass)

    assert mut_instance.x == X1
    assert mut_instance.s == S1

    mut_instance.x = X2
    assert mut_instance.x == X2

    mut_instance.s = S2
    assert mut_instance.s == S2
