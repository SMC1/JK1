#!/usr/bin/python

import sys, os, getopt, math
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH):

	print 'Usage: degSeq_process.py -i [input file dir]'
	sys.exit(0)

inputDirN = optH['-i']


inFile = os.popen('tail -q -n +2 %s/*.rpkm | cut -f3' % inputDirN)

valueL = []

for line in inFile:
	#valueL.append('%.4f' % math.log(1+float(line[:-1]),2))
	valueL.append('%.4f' % float(line[:-1]))


print '\t'.join(valueL)
