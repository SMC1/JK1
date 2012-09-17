#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def downsample(downFactor):

	inFqFile = sys.stdin
	outFqFile = sys.stdout

	count = -1

	while 1:

		count += 1

		line1 = inFqFile.readline()

		if not line1:
			break

		line2 = inFqFile.readline()
		line3 = inFqFile.readline()
		line4 = inFqFile.readline()

		if count % downFactor == 0:
			outFqFile.write(line1+line2+line3+line4)


optL, argL = getopt.getopt(sys.argv[1:],'f:',[])

optH = mybasic.parseParam(optL)

if '-f' in optH:

	downsample(int(optH['-f']))
