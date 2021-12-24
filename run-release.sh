#!/bin/bash

# see: https://gist.github.com/robin-a-meade/58d60124b88b60816e8349d1e3938615
set -eu pipefail

pip install twine

rm -rf dist

python setup.py sdist bdist_wheel --universal

twine upload dist/*

