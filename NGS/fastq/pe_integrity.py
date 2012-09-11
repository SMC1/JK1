#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def pe_integrity(fqFilePrefix):

	inFqFile1 = open('%s.1.fastq' % fqFilePrefix)
	inFqFile2 = open('%s.2.fastq' % fqFilePrefix)

	outFqFile1 = open('%s_fixed.1.fastq' % fqFilePrefix, 'w')
	outFqFile2 = open('%s_fixed.2.fastq' % fqFilePrefix, 'w')

	i1 = 0
	i2 = 0

	while 1:

		while 1:

			line = inFqFile1.readline()

			if not line:
				break

			if line[0] != '@':
				raise Exception

			if line[-3] != '/':
				print line,
				inFqFile1.readline()
				inFqFile1.readline()
				inFqFile1.readline()
				continue

			id1 = line[1:-3]
			record1 = line + inFqFile1.readline() + inFqFile1.readline() + inFqFile1.readline()

			break

		if not line:
			break

		while 1:

			line = inFqFile2.readline()

			if not line:
				break

			if line[0] != '@':
				raise Exception

			if line[-3] != '/':
				print line,
				inFqFile1.readline()
				inFqFile1.readline()
				inFqFile1.readline()
				continue

			id2 = line[1:-3]
			record2 = line + inFqFile2.readline() + inFqFile2.readline() + inFqFile2.readline()
			
			break

		if not line:
			break

		if id1==id2:
			outFqFile1.write(record1)
			outFqFile2.write(record2)
		else:
			print id1,id2
			print record1
			print record2
			sys.exit(1)

	outFqFile1.close()
	outFqFile2.close()


optL, argL = getopt.getopt(sys.argv[1:],'i:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH:

	pe_integrity(optH['-i'])
