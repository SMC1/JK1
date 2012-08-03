#!/usr/bin/python

import sys, getopt
import mybasic

optL, argL = getopt.getopt(sys.argv[1:],'i:o:l:',[])
optH = mybasic.parseParam(optL)

if '-i' in optH:
	inFileName = optH['-i']
else:
	inFileName = ''

if '-o' in optH:
	outFileName = optH['-o']
else:
	outFileName = ''

if '-l' in optH:
	numNt = int(optH['-l'])
else:
	numNt = 25


if inFileName=='' or outFileName=='':
	print 'inFile or outFile not specified'
	sys.exit(0)

inFile = open(inFileName)
outFile = open(outFileName,'w')

while 1:

	header = inFile.readline()

	if not header:
		break

	seq = inFile.readline()
	inFile.readline()
	qual = inFile.readline()

	outFile.write('%s%s\n+\n%s\n' % (header,seq[:numNt],qual[:numNt]))

outFile.close()
inFile.close()
