import pytest
from constclasses.ccerror import ConstError, InitializationError
from constclasses.static_const_class import mutable_instance, static_const_class

X1, S1 = 1, "str1"
X2, S2 = 2, "str2"


@static_const_class
class StaticConstResource:
    x: int = X1
    s: str = S1


def test_static_const_class_initialization_error():
    with pytest.raises(TypeError) as err:
        _ = StaticConstResource(X2, S2)

    err_msg = str(err.value)
    assert err_msg == "'StaticConstResource' object is not callable"


def test_static_const_class_member_modification():
    with pytest.raises(ConstError) as err:
        StaticConstResource.x = X2

    build_err_msg = (
        lambda member: f"Cannot modify const attribute `{member}` of class `StaticConstResource`"
    )

    err_msg = str(err.value)
    assert err_msg == build_err_msg("x")

    with pytest.raises(ConstError) as err:
        StaticConstResource.s = S2

    err_msg = str(err.value)
    assert err_msg == build_err_msg("s")


def test_mutable_instance_of_static_const_class():
    mut_instance = mutable_instance(StaticConstResource)

    assert mut_instance.x == X1
    assert mut_instance.s == S1

    mut_instance.x = X2
    assert mut_instance.x == X2

    mut_instance.s = S2
    assert mut_instance.s == S2


if __name__ == "__main__":
    mut_instance = mutable_instance(StaticConstResource)
