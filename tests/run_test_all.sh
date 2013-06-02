#!/usr/bin/env bash

PARAM=
if [ "$#" == "1" ]
then
  PARAM=$1
fi

if [ -e htmlcov ]
then
  rm -rf htmlcov
fi

PATH_TO_SRC=../src
OLD_PYTHONPATH=$PYTHONPATH

export PYTHONPATH=$PYTHONPATH:$PATH_TO_SRC

coverage2 run --include=../src/*.py test_all.py $PARAM

coverage2 html

export PYTHONPATH=$OLD_PYTHONPATH
rm *.pyc
