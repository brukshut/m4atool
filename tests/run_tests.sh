#!/bin/bash

cd .. 
# format python code with black
python -m black m4atool && black tests

# lint python code with flake8
python -m flake8

# run unit tests
cd tests
python -m unittest test_m4a.py
