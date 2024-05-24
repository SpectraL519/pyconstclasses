# PyConstClasses

[![tests](https://github.com/SpectraL519/pyconstclasses/actions/workflows/tests.yaml/badge.svg)](https://github.com/SpectraL519/pyconstclasses/actions/workflows/tests)
[![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/SpectraL519/f6cec4c4c8e1733cfe45f807918a128a/raw/covbadge.json)]()

<!-- TODO: github workflows -->

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

* export requirements: `pip freeze > requirements.txt`
* install requirements: `pip install -r requirements.txt`
* build distribution: `python setup.py sdist bdist_wheel`
* project venv: `cc_venv`, `test_cc_venv` (for local package installation tests)
* install package in test venv: `pip install dist/pyconstclasses-0.1-py3-none-any.whl --force-reinstall`
* test with coverage: `pytest -v constclasses/test/ --cov=constclasses --cov-report=xml --cov-report=html --junitxml=junit/test-results.xml`

<br />
<br />

## Licence

The `PyConstClasses` project uses the [MIT Licence](https://opensource.org/license/mit/)
