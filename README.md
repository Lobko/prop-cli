# prop-cli

A simple command-line tool that solves proportions of the form:

    a : b = c : d

where one of the terms is unknown (`x`).  
This is the classic **rule of three**, a fundamental arithmetic technique for solving proportions by cross-multiplication.

---

## Installation

Clone the repository and install locally:

    pip install .

This will install the `prop-cli` command.

---

## Usage

    prop-cli <a> <b> <c> <d>

Example:

    prop-cli 10 12 x 30

Output:

    Proportion: 10:12 = 25:30
    x = 25

You can put `x` in any of the four positions:

    prop-cli x 5 6 12
    prop-cli 2 x 4 8
    prop-cli 3 9 x 27
    prop-cli 4 5 0.1 x

---

## How cross-multiplication works

To solve a proportion of the form:

    a : b = c : d

we use **cross-multiplication**, which states that:

    a × d = b × c

This is the fundamental property of proportions.

### Visual ASCII diagram

       a : b = c : d
         │       │
         │       │
         └───┬───┘
             │
     Cross-multiplication
             │
       a × d = b × c

### Solving for an unknown (example)

If one term is unknown (`x`), we isolate it using the cross-multiplication identity.

Case: the unknown is in the second position (`x`):

        a : x = c : d
          │       │
          │       │
          └───┬───┘
              │
      a × d = x × c
              │
              └──→  x = (a × d) / c

Another case: unknown in the fourth position (`x`):

        a : b = c : x
          │       │
          │       │
          └───┬───┘
              │
      a × x = b × c
              │
              └──→  x = (b × c) / a

This tool automatically:
- identifies where the `x` is,
- applies the correct formula,
- prints the solved proportion and the computed value.

---

## Error handling

The tool validates:
- only one unknown term (`x`)
- all other terms must be valid numbers
- division by zero is caught with clear error messages

---

## Project structure

    prop-cli/
    ├── pyproject.toml
    ├── README.md
    └── proportion_calculator/
        ├── cli.py
        └── __init__.py

---

## License

MIT License