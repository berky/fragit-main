#!/usr/bin/env bash

all:
	python2 setup.py build
	python2 setup.py install --user

test:
	cd tests; $(MAKE) $(MFLAGS) test;

test-full:
	cd tests; $(MAKE) $(MFLAGS) test-full;
