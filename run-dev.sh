#!/bin/bash

# see: https://gist.github.com/robin-a-meade/58d60124b88b60816e8349d1e3938615
set -eu pipefail

make resolve;
pip install Flask==$FLASK;
pip install webargs!=5.0.0;
python setup.py install;

if [ "$CHECK_STYLE" = "yes" ] || [ "$CHECK_STYLE" = "1" ]; then
  make check-style;
fi

if [ "$RUN_TEST" = "yes" ] || [ "$RUN_TEST" = "1" ]; then
  make test;
  make report-coverage;
fi
