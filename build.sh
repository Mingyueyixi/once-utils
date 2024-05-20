#!/bin/bash

if [ -d "./dist" ]; then
    rm -rf ./dist/*
fi

#    pip install build
if [[ `pip list | grep "build"` ]]; then
    echo "build tools already installed"
else
    pip install build
fi

echo "building package..."
# deprecated 58.3.0
#python setup.py sdist
#https://packaging.python.org/en/latest/discussions/setup-py-deprecated/

python -m build

echo "building package completed..."





