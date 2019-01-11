#!/bin/bash

make resolve;
pip install Flask==$FLASK;
pip install webargs==4.4.1;
python setup.py install;

if [ "$CHECK_STYLE" = "yes" ] || [ "$CHECK_STYLE" = "1" ]; then
  echo "style checking...";
  make check-style;
fi

if [ "$RUN_TEST" = "yes" ] || [ "$RUN_TEST" = "1" ]; then
  echo "test running...";
  make test;
fi
