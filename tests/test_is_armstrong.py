"""Unit tests: is_armstrong called directly from libarmstrong.so."""

import ctypes
from pathlib import Path

import pytest

LIB = Path(__file__).resolve().parents[1] / "libarmstrong.so"

# Every Armstrong number that fits in a 32-bit int.
ARMSTRONG = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
    153, 370, 371, 407, 1634, 8208, 9474,
    54748, 92727, 93084, 548834, 1741725, 4210818,
    9800817, 9926315, 24678050, 24678051, 88593477,
    146511208, 472335975, 534494836, 912985153,
]

NOT_ARMSTRONG = [
    10, 11, 100, 152, 154, 372, 1000, 1633, 9475, 99999,
    912985152, 999999999, 1000000000, 2147483647, -1, -153,
]


def reference(n):
    return n >= 0 and sum(int(d) ** len(str(n)) for d in str(n)) == n


@pytest.fixture(scope="module")
def is_armstrong():
    if not LIB.exists():
        pytest.fail(f"{LIB.name} was not built, run `make` first")
    function = ctypes.CDLL(str(LIB)).is_armstrong
    function.argtypes = [ctypes.c_int]
    function.restype = ctypes.c_bool
    return function


@pytest.mark.parametrize("n", ARMSTRONG)
def test_is_armstrong_accepts(is_armstrong, n):
    assert is_armstrong(n), f"{n} is an Armstrong number"


@pytest.mark.parametrize("n", NOT_ARMSTRONG)
def test_is_armstrong_rejects(is_armstrong, n):
    assert not is_armstrong(n), f"{n} is not an Armstrong number"


def test_is_armstrong_up_to_100000(is_armstrong):
    wrong = [n for n in range(100_000) if is_armstrong(n) != reference(n)]
    assert not wrong, f"is_armstrong is wrong for {wrong[:10]}"
