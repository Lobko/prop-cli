#!/usr/bin/env python3
"""Proportion calculator for expressions of the form a:b = c:d."""

import sys
from typing import Optional


def fmt(value: float) -> str:
    """Format numbers without scientific notation."""
    s = f"{value:.12f}".rstrip("0").rstrip(".")
    return s if s != "-0" else "0"


def solve_proportion(a_str: str, b_str: str, c_str: str, d_str: str) -> Optional[float]:
    """
    Solves a proportion a:b = c:d given as strings.
    One of the four values must be 'x'.
    """
    terms = [a_str, b_str, c_str, d_str]

    # Find position of the unknown 'x'
    x_positions = [i for i, term in enumerate(terms) if term.lower() == "x"]

    if len(x_positions) == 0:
        print("Error: No 'x' found. One term must be the unknown.")
        return None
    if len(x_positions) > 1:
        print("Error: Only one unknown 'x' is allowed.")
        return None

    x_pos = x_positions[0]

    try:
        # Convert numeric values
        a, b, c, d = [None if i == x_pos else float(term) for i, term in enumerate(terms)]

        # Compute depending on the unknown position
        if x_pos == 0:
            if d == 0:
                print("Error: Division by zero (d = 0).")
                return None
            x = (b * c) / d
        elif x_pos == 1:
            if c == 0:
                print("Error: Division by zero (c = 0).")
                return None
            x = (a * d) / c
        elif x_pos == 2:
            if b == 0:
                print("Error: Division by zero (b = 0).")
                return None
            x = (a * d) / b
        else:  # x_pos == 3
            if a == 0:
                print("Error: Division by zero (a = 0).")
                return None
            x = (b * c) / a

        result = [a, b, c, d]
        result[x_pos] = x

        print(f"Proportion: {fmt(result[0])}:{fmt(result[1])} = {fmt(result[2])}:{fmt(result[3])}")
        print(f"x = {fmt(x)}")

        return x

    except ValueError:
        print("Error: Only numbers or 'x' are allowed.")
        return None


def print_usage() -> None:
    print("--- Proportion Calculator (a:b = c:d) ---")
    print("Usage: prop-cli <a> <b> <c> <d>")
    print("Example: prop-cli 10 12 x 30")
    print("Note: Use 'x' for the unknown term.")


def main() -> int:
    if len(sys.argv) != 5:
        print_usage()
        return 1

    result = solve_proportion(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    return 0 if result is not None else 1


if __name__ == "__main__":
    sys.exit(main())