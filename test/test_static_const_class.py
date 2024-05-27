import pytest
from constclasses.ccerror import ConstError, InitializationError
from constclasses.static_const_class import static_const_class


@static_const_class
class StaticConstResource:
    x: int = 1
    s: str = "str"


def test_static_const_class_initialization_error():
    x2, y2 = 2, "str2"

    with pytest.raises(TypeError) as err:
        _ = StaticConstResource(x2, y2)

    err_msg = str(err.value)
    assert err_msg == "'StaticConstResource' object is not callable"


def test_static_const_class_member_modification():
    x2, s2 = 2, "str2"

    with pytest.raises(ConstError) as err:
        StaticConstResource.x = x2

    build_err_msg = (
        lambda member: f"Cannot modify const attribute `{member}` of class `StaticConstResource`"
    )

    err_msg = str(err.value)
    assert err_msg == build_err_msg("x")

    with pytest.raises(ConstError) as err:
        StaticConstResource.s = s2

    err_msg = str(err.value)
    assert err_msg == build_err_msg("s")
