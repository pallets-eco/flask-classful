#!/bin/bash

# see: https://gist.github.com/robin-a-meade/58d60124b88b60816e8349d1e3938615
set -eu pipefail

make resolve;
pip install $REQUIREMENTS;
python setup.py install;

if [ "$CHECK_STYLE" = "yes" ] || [ "$CHECK_STYLE" = "1" ]; then
  make check-style;
fi

if [ "$RUN_TEST" = "yes" ] || [ "$RUN_TEST" = "1" ]; then
  pip install webargs
  make test;
  make report-coverage;
fi
