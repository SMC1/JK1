#!/usr/bin/python

import sys

prefixF = open(sys.argv[1])
prefixLen = int(sys.argv[2])

prefixList = []

while 1:

	l1 = prefixF.readline()

	if not l1:
		break

	prefixList.append(prefixF.readline()[:-1])

	prefixF.readline()
	prefixF.readline()

print prefixList

f = sys.stdin

while 1:

	l1 = f.readline()

	if not l1:
		break

	l2 = f.readline()

	if l2[:prefixLen] in prefixList:

		print l1,
		print l2,
		print f.readline(),
		print f.readline(),
