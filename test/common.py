from constclasses.const_class import const_class
from constclasses.static_const_class import static_const_class

X1, S1 = 1, "str1"
X2, S2 = 2, "str2"

X_ATTR_NAME = "x"
S_ATTR_NAME = "s"


@const_class
class ConstClass:
    x: int
    s: str


@static_const_class
class StaticConstClass:
    x: int = X1
    s: str = S1
