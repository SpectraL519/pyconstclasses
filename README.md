# PyConstClasses

[![tests](https://github.com/SpectraL519/pyconstclasses/actions/workflows/tests.yaml/badge.svg)](https://github.com/SpectraL519/pyconstclasses/actions/workflows/tests)
[![format](https://github.com/SpectraL519/pyconstclasses/actions/workflows/format.yaml/badge.svg)](https://github.com/SpectraL519/pyconstclasses/actions/workflows/format)
[![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/SpectraL519/f6cec4c4c8e1733cfe45f807918a128a/raw/covbadge.json)]()

> [!IMPORTANT]
> This readme file will be extended later in the development process

<br />

## Overview

`PyConstClasses` is a python package containing const class decorators and utility. It allows for the creation constant and static constant classes by utilizing the annotations of the

<br />
<br />

## Table of contents

* Installation
* Tutorial
* Examples
* [Dev notes](#dev-notes)
* [Licence](#licence)

<br />
<br />

## Dev notes

* export requirements: `pip freeze > requirements-dev.txt`
* install requirements: `pip install -r requirements-dev.txt`
* build distribution: `python -m build` (`pip install build`)
* project venv: `cc_venv`, `test_cc_venv` (for local package installation tests)
* install package in test venv: `pip install dist/pyconstclasses-<version>-py3-none-any.whl --force-reinstall`
* test with coverage: `pytest -v constclasses/test/ --cov=constclasses --cov-report=xml --cov-report=html` or `tox`
* format:
    * `black .` or `python -m black .` (`--check`)
    * `isort .` or `python -m isort .` (`--check`)

<br />
<br />

## Licence

The `PyConstClasses` project uses the [MIT Licence](https://opensource.org/license/mit/)
