from itertools import permutations
from dialogos import *


# Test the functions for processing strings.


def test_calc_for_none() -> None:
    values = ("", "(", ")", "()", "(())", "+", "*", "vim", "nim", "-1", "+1")
    for l, r in permutations(values, 2):
        for op in values:
            s = f"{l}{op}{r}"
            assert calc(s) is None


def test_calc_for_some() -> None:
    values = (
        "0",
        "11",
        "22 * 10",
        "(35)",
        "((17))",
        "(1 + 1)",
        "((17 - 29))",
        "(53 + 23 / (78 + 14 * (94 * 2) + 3))",
    )
    ops = ("+", "*")
    for l, r in permutations(values, 2):
        for op in ops:
            s = f"{l}{op}{r}"
            n1 = calc(l)
            n2 = calc(r)
            n3 = calc(s)
            if n1 is not None and n2 is not None and n3 is not None:
                if op == "+":
                    assert n3 == n1 + n2
                elif op == "*":
                    assert n3 == n1 * n2
            else:
                assert False


def test_split() -> None:
    assert split("") == [""]
    assert split("   orb|| bro  ") == ["orb", " bro"]


# TODO: Test the dialogue struct.
