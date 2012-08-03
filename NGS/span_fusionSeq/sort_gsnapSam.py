#!/usr/bin/python

import sys

inFile = open(sys.argv[1])

while 1:

	line1 = inFile.readline()

	if not line1:
		break

	if line1[0] == '@':
		print line1,
		continue

	line2 = inFile.readline()

	tokL1 = line1.split('\t')
	tokL2 = line2.split('\t')

	if (tokL1[2] == tokL2[2] and int(tokL1[3]) > int(tokL2[3])) or tokL1[2] > tokL2[2]:
		line1,line2 = line2,line1

	print line1,
	print line2,

inFile.close()
