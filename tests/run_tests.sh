#!/bin/bash

cd .. 
# Format python code with black.
for dir in m4atool tests; do
    python -m black $dir
done

# Lint python code with flake8.
for dir in m4atool tests; do
    python -m flake8 $dir
done

# Perform static type checking with mypy
python -m mypy m4atool

# run unit tests
cd tests
python -m unittest test_m4a.py
