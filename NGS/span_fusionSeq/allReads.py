#!/usr/bin/python

import sys

f = sys.stdin

while 1:

	l1 = f.readline()

	if not l1:
		break

	print f.readline(),

	f.readline()
	f.readline()
