# prop-cli

[![PyPI version](https://img.shields.io/pypi/v/prop-cli)](https://pypi.org/project/prop-cli/)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/pypi/pyversions/prop-cli)
![Downloads](https://img.shields.io/pypi/dm/prop-cli)
![Tests](https://github.com/Lobko/prop-cli/actions/workflows/test.yml/badge.svg)
![Lint](https://github.com/Lobko/prop-cli/actions/workflows/lint.yml/badge.svg)
![Build](https://github.com/Lobko/prop-cli/actions/workflows/build.yml/badge.svg)

A command-line tool that solves proportions of the form:

```
a : b = c : d
```

where one term is unknown (`x`).  
The tool uses classic **cross-multiplication**, also known as the **rule of three**.

---

## Installation

```
pip install prop-cli
```

This installs the command:

```
prop-cli
```

### Installing from source (local clone)

If you clone this repository manually:

```
git clone https://github.com/Lobko/prop-cli
cd prop-cli
```

You can install the package locally with:

```
pip install .
```

Or, if you want to install it in development/editable mode:

```
pip install -e .
```

This allows you to modify the source code and use the `prop-cli` command immediately without rebuilding the package.

---

## Usage

```
prop-cli <a> <b> <c> <d>
```

Example:

```
prop-cli 10 12 x 30
```

Output:

```
Proportion: 10:12 = 25:30
x = 25
```

You can place `x` in any position:

```
prop-cli x 5  6  12
prop-cli 2 x  4   8
prop-cli 3 9  x  27
prop-cli 4 5 0.1  x
```

---

## More Examples

```
prop-cli 5 20 x 120     # x = 30
prop-cli x 4 12 48      # x = 1
prop-cli 3 x  9 15      # x = 5
```

### Edge cases (real ones)

```
prop-cli 1 x 0 5        # division by zero (c = 0)
prop-cli x 0 3 2        # division by zero (b = 0)
prop-cli 1 2 3 x        # valid
```

---

## How cross-multiplication works

Given the proportion:

```
a : b = c : d
```

Rule:

```
a × d = b × c
```

### Diagram (horizontal)

```
       a : b = c : d
         |       |
         |       |
         +---+---+
             |
   Cross-multiplication
             |
       a × d = b × c
```

### Diagram (vertical rule-of-three)

```
     a      c
     ─── = ───
     b      d

Cross multiply:

a × d = b × c
```

---

## Solving when the unknown is in different positions

### Unknown in second position

```
a : x = c : d
a × d = x × c
x = (a × d) / c
```

### Unknown in fourth position

```
a : b = c : x
a × x = b × c
x = (b × c) / a
```

---

## Error handling

- Exactly one unknown `x` is required  
- Other terms must be numeric  
- Division by zero is detected and reported  
- Scientific notation is avoided in output  

---

## Project structure

```
prop-cli/
├── pyproject.toml
├── README.md
├── LICENSE
├── CHANGELOG.md
├── VERSION
├── tests/
│   └── test_basic.py
├── .github/
│   └── workflows/
│       ├── test.yml
│       ├── lint.yml
│       └── build.yml
└── proportion_calculator/
    ├── cli.py
    └── __init__.py
```

---

## Contributing

1. Fork the repository  
2. Create a feature branch  
3. Commit your changes  
4. Push the branch  
5. Open a Pull Request  

---

## License

MIT License