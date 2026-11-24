import subprocess
import sys

import pytest

from proportion_calculator import __version__
from proportion_calculator.cli import (
    ProportionError,
    fmt,
    main,
    solve,
    solve_proportion,
)


@pytest.mark.parametrize(
    "terms, expected",
    [
        # x in every position
        (["x", "5", "6", "12"], [2.5, 5, 6, 12]),
        (["2", "x", "4", "8"], [2, 4, 4, 8]),
        (["10", "12", "x", "30"], [10, 12, 25, 30]),
        (["4", "5", "0.1", "x"], [4, 5, 0.1, 0.125]),
        # examples from the README
        (["5", "20", "x", "120"], [5, 20, 30, 120]),
        (["x", "4", "12", "48"], [1, 4, 12, 48]),
        (["3", "x", "9", "15"], [3, 5, 9, 15]),
        (["1", "2", "3", "x"], [1, 2, 3, 6]),
        # negatives, zero as first term, upper-case X, scientific notation
        (["-4", "2", "x", "3"], [-4, 2, -6, 3]),
        (["x", "4", "0", "7"], [0, 4, 0, 7]),
        (["X", "5", "6", "12"], [2.5, 5, 6, 12]),
        (["1e3", "2", "x", "4"], [1000, 2, 2000, 4]),
    ],
)
def test_solve(terms, expected):
    assert solve(terms) == pytest.approx(expected)


@pytest.mark.parametrize(
    "terms, message",
    [
        (["1", "2", "3", "4"], "No 'x' found"),
        (["x", "x", "3", "4"], "Only one unknown"),
        (["x", "abc", "3", "4"], "Invalid value for b"),
        (["x", "1", "inf", "4"], "Only finite numbers"),
        (["x", "1", "nan", "4"], "Only finite numbers"),
        (["x", "0", "3", "2"], "b cannot be 0"),
        (["1", "2", "x", "0"], "d cannot be 0"),
        (["1", "x", "0", "5"], "c = 0"),
        (["0", "2", "3", "x"], "a = 0"),
        (["0", "x", "3", "5"], "No solution: b would be 0"),
        (["1e308", "1e-308", "x", "10"], "too large"),
        (["1", "2", "3"], "Exactly four terms"),
    ],
)
def test_solve_errors(terms, message):
    with pytest.raises(ProportionError, match=message):
        solve(terms)


# --- fmt --------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        (25.0, "25"),
        (2.5, "2.5"),
        (-6.0, "-6"),
        (-0.0, "0"),
        (0.1 * 3, "0.3"),
        (1 / 3, "0.333333333333333"),
        (1e-15, "0.000000000000001"),
        (1e20, "100000000000000000000"),
    ],
)
def test_fmt(value, expected):
    assert fmt(value) == expected


# --- command line -----------------------------------------------------------

def test_main_success(capsys):
    assert main(["10", "12", "x", "30"]) == 0
    out, err = capsys.readouterr()
    assert out == "Proportion: 10:12 = 25:30\nx = 25\n"
    assert err == ""


def test_main_error_goes_to_stderr(capsys):
    assert main(["1", "x", "0", "5"]) == 1
    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith("Error: ")


@pytest.mark.parametrize("flag", ["-h", "--help"])
def test_main_help(capsys, flag):
    assert main([flag]) == 0
    assert "usage: prop-cli" in capsys.readouterr().out


@pytest.mark.parametrize("flag", ["-V", "--version"])
def test_main_version(capsys, flag):
    assert main([flag]) == 0
    assert capsys.readouterr().out == f"prop-cli {__version__}\n"


def test_main_wrong_number_of_arguments(capsys):
    assert main(["1", "2", "x"]) == 2
    out, err = capsys.readouterr()
    assert out == ""
    assert "usage: prop-cli" in err


def test_negative_scientific_number_is_not_an_option(capsys):
    assert main(["-1e2", "2", "x", "4"]) == 0
    assert "x = -200" in capsys.readouterr().out


def test_solve_proportion_backward_compatible(capsys):
    assert solve_proportion("10", "12", "x", "30") == 25
    assert solve_proportion("1", "2", "3", "4") is None


def test_module_is_runnable():
    result = subprocess.run(
        [sys.executable, "-m", "proportion_calculator.cli",
         "2", "x", "4", "8"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout.endswith("x = 4\n")
