#!/bin/bash

python setup.py install;
make resolve;
pip uninstall -y Flask;
pip install Flask==$FLASK;

if [ "$CHECK_STYLE" = "yes" ] || [ "$CHECK_STYLE" = "1" ]; then
  echo "style checking...";
  make check-style;
fi

if [ "$RUN_TEST" = "yes" ] || [ "$RUN_TEST" = "1" ]; then
  echo "test running...";
  make test;
fi
