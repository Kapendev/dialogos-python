from dialogos import *

# TODO: Add more tests.

def test_calc():
    assert calc("") is None
    assert calc("ada") is None
    assert calc("oh+wow") is None
    assert calc("oh*wow") is None
    assert calc("()") is None
    assert calc("()+()") is None
    assert calc("()*()") is None
    assert calc("1") == 1.0
    assert calc("(1)") == 1.0
    assert calc("((1))") == 1.0
