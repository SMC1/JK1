#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def trim(inFqFileName,outFqFilePrefix,trimLen,pairedEnd=True):

	if inFqFileName == 'stdin':
		inFqFile = sys.stdin
	else:
		inFqFile = open(inFqFileName)

	if outFqFilePrefix == 'stdout':
		outFqFile = sys.stdout
	else:
		if pairedEnd:
			rm = re.search('(.*)\.([12])',outFqFilePrefix.split('/')[-1])
			outFqFile = open('%s_%snt.%s.fastq' % (rm.group(1),trimLen,rm.group(2)), 'w')
		else:
			outFqFile = open('%s_%snt.fastq' % (outFqFilePrefix,trimLen), 'w')

	while 1:

		line = inFqFile.readline()

		if not line:
			break

		seq = inFqFile.readline()[:-1]

		if line[0] != '@':
			raise Exception

		seqN = line[1:].rstrip().split(' ')[0]

		inFqFile.readline()
		
		qual = inFqFile.readline()[:-1]
		
#		if 'N' in seq[:trimLen]:
#			continue

		outFqFile.write('@%s\n%s\n+\n%s\n' % (seqN,seq[:trimLen],qual[:trimLen]))

	outFqFile.close()


optL, argL = getopt.getopt(sys.argv[1:],'i:o:l:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH and '-l' in optH:

	trim(optH['-i'], optH['-o'], int(optH['-l']))
