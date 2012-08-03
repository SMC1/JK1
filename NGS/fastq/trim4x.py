#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def trim4x(inFqFileName,outFqFilePrefix,trimLen):

	if inFqFileName == 'stdin':
		inFqFile = sys.stdin
	else:
		inFqFile = open(inFqFileName)

	outFqFile1 = open('%s.1.fastq' % outFqFilePrefix, 'w')
	outFqFile2 = open('%s.2.fastq' % outFqFilePrefix, 'w')

	while 1:

		line = inFqFile.readline()

		if not line:
			break

		seq = inFqFile.readline()[:-1]

		if line[0] != '@':
			raise Exception

		seqN = line[1:].rstrip().split(' ')[0]

		inFqFile.readline(); 
		
		qual = inFqFile.readline()[:-1]
		
		if 'N' in seq[:trimLen] or 'N' in seq[-trimLen:]:
			continue

		outFqFile1.write('@%s/1\n%s\n+\n%s\n' % (seqN,seq[:trimLen],qual[:trimLen]))
		outFqFile2.write('@%s/2\n%s\n+\n%s\n' % (seqN,mybasic.rc(seq[-trimLen:]),mybasic.rev(qual[-trimLen:])))

	outFqFile1.close()
	outFqFile2.close()


optL, argL = getopt.getopt(sys.argv[1:],'i:o:l:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH and '-l' in optH:

	trim4x(optH['-i'], optH['-o'], int(optH['-l']))
