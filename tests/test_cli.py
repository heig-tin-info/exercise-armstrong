"""Functional tests of the armstrong program, run as a user would."""

import subprocess
from pathlib import Path

import pytest

EXEC = Path(__file__).resolve().parents[1] / "armstrong"

ARMSTRONG = [0, 9, 153, 9474, 912985153]
NOT_ARMSTRONG = [10, 33, 154, 9475, 2147483647, -153]


def run(*args, stdin=""):
    return subprocess.run(
        [str(EXEC), *map(str, args)],
        input=stdin,
        capture_output=True,
        text=True,
        timeout=10,
    )


def message(n, armstrong):
    verb = "est" if armstrong else "n'est pas"
    return f"Le nombre {n} {verb} un nombre d'Armstrong."


@pytest.fixture(scope="module", autouse=True)
def executable():
    if not EXEC.exists():
        pytest.fail(f"{EXEC.name} was not built, run `make` first")


# ---------- Number as an argument ----------
@pytest.mark.parametrize("n", ARMSTRONG)
def test_argument_armstrong_exits_with_0(n):
    assert run(n).returncode == 0


@pytest.mark.parametrize("n", NOT_ARMSTRONG)
def test_argument_not_armstrong_exits_with_1(n):
    assert run(n).returncode == 1


@pytest.mark.parametrize("n", [153, 154])
def test_argument_prints_the_result(n):
    assert run(n).stdout.strip() == message(n, n == 153)


# ---------- Number on stdin ----------
@pytest.mark.parametrize("n", [9, 153, 9474])
def test_stdin_armstrong_exits_with_0(n):
    assert run(stdin=f"{n}\n").returncode == 0


@pytest.mark.parametrize("n", [10, 154])
def test_stdin_not_armstrong_exits_with_1(n):
    assert run(stdin=f"{n}\n").returncode == 1


@pytest.mark.parametrize("n", [153, 154])
def test_stdin_prints_the_result(n):
    assert run(stdin=f"{n}\n").stdout.strip() == message(n, n == 153)


# ---------- Invalid input ----------
INVALID = {
    "word argument": dict(args=["foo"]),
    "two arguments": dict(args=[153, 154]),
    "word on stdin": dict(stdin="foo\n"),
    "empty stdin": dict(stdin=""),
}


@pytest.mark.parametrize("case", INVALID.values(), ids=INVALID.keys())
def test_invalid_input_exits_with_2(case):
    assert run(*case.get("args", []), stdin=case.get("stdin", "")).returncode == 2


@pytest.mark.parametrize("case", INVALID.values(), ids=INVALID.keys())
def test_invalid_input_explains_on_stderr(case):
    process = run(*case.get("args", []), stdin=case.get("stdin", ""))
    assert process.stderr.strip(), "Expected an error message on stderr"
    assert not process.stdout.strip(), "Expected nothing on stdout"
