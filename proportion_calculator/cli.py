"""Proportion calculator for expressions of the form a:b = c:d."""

import math
import sys
from collections.abc import Sequence
from decimal import Decimal

from proportion_calculator import __version__

UNKNOWN = "x"
NAMES = ("a", "b", "c", "d")
SIGNIFICANT_DIGITS = 15

USAGE = """\
usage: prop-cli <a> <b> <c> <d>

Solve the proportion a:b = c:d, where exactly one term is the unknown 'x'.

options:
  -h, --help     show this help message and exit
  -V, --version  show the version and exit

examples:
  prop-cli 10 12 x 30     # x = 25
  prop-cli x 5 6 12       # x = 2.5
"""


class ProportionError(ValueError):
    """Raised when the input does not describe a solvable proportion."""


def fmt(value: float) -> str:
    """Format a number in plain decimal notation (no scientific notation).

    The value is rounded to 15 significant digits, which hides floating
    point noise (0.1 * 3 is shown as 0.3) without losing small values
    (1e-15 is shown as 0.000000000000001, not 0).
    """
    number = Decimal(f"{value:.{SIGNIFICANT_DIGITS}g}")
    if number == 0:
        return "0"
    text = format(number, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def parse_terms(terms: Sequence[str]) -> tuple[list[float | None], int]:
    """Parse the four terms and return (values, position of 'x').

    The unknown term is returned as ``None``.
    """
    if len(terms) != 4:
        raise ProportionError("Exactly four terms are required: a b c d.")

    x_positions = [
        i for i, term in enumerate(terms)
        if term.strip().lower() == UNKNOWN
    ]
    if not x_positions:
        raise ProportionError("No 'x' found. One term must be the unknown.")
    if len(x_positions) > 1:
        raise ProportionError("Only one unknown 'x' is allowed.")
    x_pos = x_positions[0]

    values: list[float | None] = []
    for i, (name, term) in enumerate(zip(NAMES, terms)):
        if i == x_pos:
            values.append(None)
            continue
        try:
            value = float(term)
        except ValueError:
            raise ProportionError(
                f"Invalid value for {name}: '{term}'. "
                "Only numbers or 'x' are allowed."
            ) from None
        if not math.isfinite(value):
            raise ProportionError(
                f"Invalid value for {name}: '{term}'. "
                "Only finite numbers are allowed."
            )
        values.append(value)

    return values, x_pos


def solve(terms: Sequence[str]) -> list[float]:
    """Solve a:b = c:d and return the four terms with 'x' filled in.

    ``terms`` are the four terms as strings, exactly one of them 'x'.
    Raises ProportionError if the proportion cannot be solved.

    >>> solve(["10", "12", "x", "30"])
    [10.0, 12.0, 25.0, 30.0]
    """
    return _solve(terms)[0]


def _solve(terms: Sequence[str]) -> tuple[list[float], int]:
    values, x_pos = parse_terms(terms)

    # The second term of a ratio (b or d) can never be 0: a:0 is undefined.
    for i in (1, 3):
        if i != x_pos and values[i] == 0:
            raise ProportionError(
                f"{NAMES[i]} cannot be 0: a ratio with 0 as its second "
                "term is undefined."
            )

    a, b, c, d = values
    # Cross-multiplication: a * d = b * c
    if x_pos == 0:
        x = (b * c) / d
    elif x_pos == 1:
        if c == 0:
            raise ProportionError(
                "No unique solution: c = 0 (division by zero)."
            )
        x = (a * d) / c
    elif x_pos == 2:
        x = (a * d) / b
    else:
        if a == 0:
            raise ProportionError(
                "No unique solution: a = 0 (division by zero)."
            )
        x = (b * c) / a

    if not math.isfinite(x):
        raise ProportionError("The result is too large to be represented.")
    if x_pos in (1, 3) and x == 0:
        raise ProportionError(
            f"No solution: {NAMES[x_pos]} would be 0, which makes the "
            "ratio undefined."
        )

    values[x_pos] = x
    return values, x_pos


def solve_proportion(
    a_str: str,
    b_str: str,
    c_str: str,
    d_str: str
) -> float | None:
    """Solve and print a proportion; return x, or None on error.

    Kept for backward compatibility with version 1.0.x.
    """
    try:
        values, x_pos = _solve([a_str, b_str, c_str, d_str])
    except ProportionError as error:
        print(f"Error: {error}", file=sys.stderr)
        return None
    print_result(values, x_pos)
    return values[x_pos]


def print_result(values: Sequence[float], x_pos: int) -> None:
    """Print the solved proportion and the value of x."""
    a, b, c, d = (fmt(v) for v in values)
    print(f"Proportion: {a}:{b} = {c}:{d}")
    print(f"x = {fmt(values[x_pos])}")


def print_usage(file=None) -> None:
    """Print the help text (to stdout unless another file is given)."""
    print(USAGE, end="", file=file)


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point of the prop-cli command. Returns the exit code."""
    args = list(sys.argv[1:] if argv is None else argv)

    if len(args) == 1 and args[0] in ("-h", "--help"):
        print_usage()
        return 0
    if len(args) == 1 and args[0] in ("-V", "--version"):
        print(f"prop-cli {__version__}")
        return 0
    if len(args) != 4:
        print_usage(file=sys.stderr)
        return 2

    try:
        values, x_pos = _solve(args)
    except ProportionError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print_result(values, x_pos)
    return 0


if __name__ == "__main__":
    sys.exit(main())
