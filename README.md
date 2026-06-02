# Napr

[![license](https://img.shields.io/github/license/smortezah/napr)](https://github.com/smortezah/napr/blob/main/LICENSE)
[![python](https://img.shields.io/pypi/pyversions/napr)](https://img.shields.io/pypi/pyversions/napr)
[![pypi](https://img.shields.io/pypi/v/napr)](https://pypi.org/project/napr)
[![codecov](https://codecov.io/gh/smortezah/napr/branch/main/graph/badge.svg?token=DIZ6JRWAZM)](https://codecov.io/gh/smortezah/napr)
[![downloads](https://static.pepy.tech/personalized-badge/napr?period=total&units=international_system&left_color=grey&right_color=yellow&left_text=downloads)](https://pepy.tech/project/napr)
[![ci](https://github.com/smortezah/napr/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/smortezah/napr/actions/workflows/ci.yml)

Napr is a Python package that takes a machine learning driven approach to navigate the natural products chemical space.

## Install

```sh
pip install napr

# Or
# uv add napr
```

To update napr to the latest version, add -U or --upgrade flag, i.e. `pip install -U napr`.

## Tutorials

The tutorials directory include:

- [Terpene-explore](https://github.com/smortezah/napr/tree/main/tutorials/Terpene-explore.ipynb): exploratory data analysis of terpenes (the COCONUT dataset) in the natural products chemical space
- [Terpene-classification-classic](https://github.com/smortezah/napr/tree/main/tutorials/Terpene-classification-classic.ipynb): classification of terpenes with ML techniques such as kNN, random forest and xgboost

## Development

We welcome new contributors of all experience levels.

### Testing

Launch the test suite, after installation:

```sh
pytest
```

## Cite

If you use this package, please cite:

> Hosseini, M.; Pereira, D.M. The Chemical Space of Terpenes: Insights from Data Science and AI. *Pharmaceuticals* **2023**, 16, 202. https://doi.org/10.3390/ph16020202
