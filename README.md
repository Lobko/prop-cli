# prop-cli

[![PyPI version](https://img.shields.io/pypi/v/prop-cli)](https://pypi.org/project/prop-cli/)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/pypi/pyversions/prop-cli)
![Downloads](https://img.shields.io/pypi/dm/prop-cli)
![Tests](https://github.com/Lobko/prop-cli/actions/workflows/test.yml/badge.svg)
![Lint](https://github.com/Lobko/prop-cli/actions/workflows/lint.yml/badge.svg)
![Build](https://github.com/Lobko/prop-cli/actions/workflows/build.yml/badge.svg)

A command-line tool that solves proportions of the form:

    a : b = c : d

where one term is unknown (x).  
This uses the classic rule of three, based on cross-multiplication.

---

## Installation

    pip install prop-cli

This installs the command:

    prop-cli

---

## Usage

    prop-cli <a> <b> <c> <d>

Example:

    prop-cli 10 12 x 30

Output:

    Proportion: 10:12 = 25:30
    x = 25

You can place x in any position:

    prop-cli x 5  6  12
    prop-cli 2 x  4   8
    prop-cli 3 9  x  27
    prop-cli 4 5 0.1  x

---

## More Examples

    prop-cli 5 20 x 120   # x = 30
    prop-cli x 4 12 48    # x = 1
    prop-cli 3 x  9 15    # x = 5

Edge cases:

    prop-cli 1 2 3 x      # ok
    prop-cli 1 0 3 x      # division by zero

---

## How cross-multiplication works

Given:

    a : b = c : d

Rule:

    a × d = b × c

Diagram:

           a : b = c : d
             |       |
             |       |
             +---+---+
                 |
       Cross-multiplication
                 |
           a × d = b × c

Unknown in second position:

    a : x = c : d
    a × d = x × c
    x = (a × d) / c

Unknown in fourth position:

    a : b = c : x
    a × x = b × c
    x = (b × c) / a

---

## Error handling

- One unknown x
- Other terms must be numeric
- Prevents division by zero
- Avoids scientific notation

---

## Project structure

    prop-cli/
    ├── pyproject.toml
    ├── README.md
    ├── LICENSE
    ├── CHANGELOG.md
    ├── VERSION
    └── proportion_calculator/
        ├── cli.py
        └── __init__.py

---

## Contributing

    1. Fork the repo
    2. git checkout -b feature/my-feature
    3. Commit changes
    4. Push branch
    5. Open Pull Request

---

## License

MIT License