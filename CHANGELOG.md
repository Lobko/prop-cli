# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/).

## [1.1.0] - 2026-11-24

### Added
- `--help` / `-h` and `--version` / `-V` options.
- `solve()` function and `ProportionError` exception, so the solver can be
  used from Python without parsing printed output.
- A real test suite (pytest) covering every position of `x`, the README
  examples, the error cases and the output formatting.
- Tests run on Python 3.10–3.14 in CI. The build workflow also installs the
  built wheel and runs it.
- Project URLs, keywords, license and Python version classifiers in the
  package metadata.

### Changed
- Error messages are now printed to stderr instead of stdout.
- Wrong number of arguments now exits with code 2 (was 1). `--help` exits
  with code 0 (was 1).
- Numbers are shown rounded to 15 significant digits instead of 12 decimal
  places. Very small values are no longer shown as `0`, and very large values
  no longer show floating-point noise.
- The version number now lives only in `proportion_calculator/__init__.py`.
  The `VERSION` file was removed.
- Python 3.10 or newer is now required. Python 3.6–3.9 have reached end of
  life. Version 1.0.2 is still available for older Pythons.
- README rewritten: corrected examples, clearer cross-multiplication
  explanation, formulas for all four positions, exit codes, development guide.

### Fixed
- `b = 0` or `d = 0` (for example `prop-cli x 0 3 2`) printed the invalid
  proportion `0:0 = 3:2` instead of reporting an error.
- A computed `b` or `d` of 0 (for example `prop-cli 0 x 3 5`) is now reported
  as having no solution.
- `inf`, `nan` and results that overflow (for example
  `prop-cli 1e308 1e-308 x 10`) were accepted and printed as `inf` or `nan`.
- Very small numbers (for example `1e-15`) were displayed as `0`.

## [1.0.2] - 2025-11-20

### Changed
- Version number aligned across `pyproject.toml`, `VERSION` and
  `__init__.py`.
- README: added "Installing from source", fixed examples and diagrams.

## [1.0.1] - 2025-11-20

### Changed
- Package description updated and README shown on PyPI.
- Code style fixes (flake8).
- Added GitHub Actions workflows for tests, lint and build.

## [1.0.0] - 2025-11-20

### Added
- First stable version of `prop-cli`.
- Command-line interface for solving proportions (rule of three).
- Automatic detection of the unknown value `x`.
- Cross-multiplication solver with formatted output.
- Error handling for invalid input and division by zero.
- ASCII diagrams explaining the rule of three.
- English documentation.
- MIT License.

[1.1.0]: https://github.com/Lobko/prop-cli/compare/5192619...HEAD
[1.0.2]: https://pypi.org/project/prop-cli/1.0.2/
[1.0.1]: https://pypi.org/project/prop-cli/1.0.1/
[1.0.0]: https://pypi.org/project/prop-cli/1.0.0/
