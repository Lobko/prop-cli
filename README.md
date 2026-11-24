# prop-cli

[![PyPI version](https://img.shields.io/pypi/v/prop-cli)](https://pypi.org/project/prop-cli/)
[![Python Version](https://img.shields.io/pypi/pyversions/prop-cli)](https://pypi.org/project/prop-cli/)
[![License](https://img.shields.io/pypi/l/prop-cli)](https://github.com/Lobko/prop-cli/blob/main/LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/prop-cli)](https://pypi.org/project/prop-cli/)
[![Tests](https://github.com/Lobko/prop-cli/actions/workflows/test.yml/badge.svg)](https://github.com/Lobko/prop-cli/actions/workflows/test.yml)
[![Lint](https://github.com/Lobko/prop-cli/actions/workflows/lint.yml/badge.svg)](https://github.com/Lobko/prop-cli/actions/workflows/lint.yml)
[![Build](https://github.com/Lobko/prop-cli/actions/workflows/build.yml/badge.svg)](https://github.com/Lobko/prop-cli/actions/workflows/build.yml)

A small command-line tool that solves proportions of the form

```
a : b = c : d
```

where one of the four terms is the unknown `x`.
It uses classic **cross-multiplication**, also known as the **rule of three**.

```
$ prop-cli 10 12 x 30
Proportion: 10:12 = 25:30
x = 25
```

---

## Installation

Requires Python 3.10 or newer. No other dependencies.

```
pip install prop-cli
```

or, to keep it isolated from your other Python packages:

```
pipx install prop-cli
```

Both install the `prop-cli` command.

### Installing from source

```
git clone https://github.com/Lobko/prop-cli
cd prop-cli
pip install .
```

Use `pip install -e .` instead for an editable (development) install, so changes
to the source code take effect immediately without reinstalling.

---

## Usage

```
prop-cli <a> <b> <c> <d>
prop-cli --help       # or -h
prop-cli --version    # or -V
```

Write `x` (or `X`) for the unknown term. It can be in any position:

```
prop-cli x 5 6 12       # x = 2.5
prop-cli 2 x 4 8        # x = 4
prop-cli 10 12 x 30     # x = 25
prop-cli 4 5 0.1 x      # x = 0.125
```

More examples:

```
prop-cli 5 20 x 120     # x = 30
prop-cli x 4 12 48      # x = 1
prop-cli 3 x 9 15       # x = 5
prop-cli -4 2 x 3       # x = -6   (negative numbers work)
prop-cli 1e3 2 x 4      # x = 2000 (so does scientific notation)
```

Results are shown in plain decimal notation (never `1e-05`), rounded to
15 significant digits, so tiny floating-point errors disappear:

```
prop-cli 1 3 x 1        # x = 0.333333333333333
prop-cli 0.1 1 x 3      # x = 0.3
```

### Errors and exit codes

Error messages are printed to **stderr**, so they don't mix with the result if
you redirect or pipe the output.

| Exit code | Meaning                                              |
|-----------|------------------------------------------------------|
| `0`       | Success (also for `--help` and `--version`)          |
| `1`       | The input is not a solvable proportion (see below)   |
| `2`       | Wrong number of arguments (the usage text is shown)  |

Inputs that are rejected:

```
prop-cli 1 2 3 4        # no 'x'
prop-cli x x 3 4        # more than one 'x'
prop-cli x abc 3 4      # not a number
prop-cli x 1 inf 4      # infinity / nan are not allowed
prop-cli x 0 3 2        # b = 0: a ratio like a:0 is undefined
prop-cli 1 2 x 0        # d = 0: same reason
prop-cli 1 x 0 5        # c = 0: no unique solution (division by zero)
prop-cli 0 2 3 x        # a = 0: no unique solution (division by zero)
```

---

## How cross-multiplication works

A proportion says that two ratios are equal:

```
a     c
─  =  ─
b     d
```

In `a : b = c : d`, the outer terms `a` and `d` are called the **extremes**
and the inner terms `b` and `c` are the **means**:

```
    ┌──── extremes ─────┐
    a  :  b   =   c  :  d
          └─means─┘
```

**Rule:** the product of the extremes equals the product of the means.

```
a × d = b × c
```

Solving this equation for the unknown gives one formula per position:

| Unknown | Proportion      | Formula             |
|---------|-----------------|---------------------|
| `a`     | `x : b = c : d` | `x = (b × c) / d`   |
| `b`     | `a : x = c : d` | `x = (a × d) / c`   |
| `c`     | `a : b = x : d` | `x = (a × d) / b`   |
| `d`     | `a : b = c : x` | `x = (b × c) / a`   |

Worked example, `10 : 12 = x : 30`:

```
x = (10 × 30) / 12 = 300 / 12 = 25
```

---

## Using it from Python

The solver can also be imported:

```python
from proportion_calculator.cli import ProportionError, solve

solve(["10", "12", "x", "30"])   # -> [10.0, 12.0, 25.0, 30.0]

try:
    solve(["x", "0", "3", "2"])
except ProportionError as error:
    print(error)                  # b cannot be 0: ...
```

---

## Development

```
git clone https://github.com/Lobko/prop-cli
cd prop-cli
pip install -e . pytest flake8

pytest                                # run the tests
flake8 proportion_calculator tests    # run the linter
```

The version number is kept only in `proportion_calculator/__init__.py`.
The packaging reads it from there.

GitHub Actions runs the tests on Python 3.10–3.14, plus the linter and a
package build check, on every push and pull request.

### Project structure

```
prop-cli/
├── proportion_calculator/
│   ├── __init__.py        # package version
│   └── cli.py             # solver and command-line interface
├── tests/
│   └── test_cli.py
├── .github/workflows/
│   ├── test.yml
│   ├── lint.yml
│   └── build.yml
├── pyproject.toml
├── CHANGELOG.md
├── LICENSE
└── README.md
```

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes (with tests)
4. Push the branch
5. Open a Pull Request

---

## License

[MIT](https://github.com/Lobko/prop-cli/blob/main/LICENSE) © Domenico Bruno "Lobkowitz"
