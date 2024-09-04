#!/bin/bash

echo Cleaning the build files...

find . -type d -name "__pycache__" -exec rm -r {} +
rm -r .pytest_cache/ .tox/ .coverage htmlcov/ coverage.* src/pyconstclasses.egg-info/ dist/
