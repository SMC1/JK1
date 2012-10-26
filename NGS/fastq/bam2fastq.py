#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def bam2fastq(inBamFileName,outFqPrefixName):

	samFile = os.popen('samtools view %s' % inBamFileName)

	outFqFile1 = open('%s.1.fastq' % outFqPrefixName, 'w')
	outFqFile2 = open('%s.2.fastq' % outFqPrefixName, 'w')

	prev1 = ''
	prev2 = ''

	for line in samFile:

		tokL = line.split('\t')

		id,seq,qual = tokL[0],tokL[9],tokL[10]

		if id[-2:] == '/1':
			
			if id != prev1:

				outFqFile1.write('@%s\n%s\n+\n%s\n' % (id,seq,qual))
				prev1 = id

		elif id[-2:] == '/2':
			
			if id != prev2:

				outFqFile2.write('@%s\n%s\n+\n%s\n' % (id,seq,qual))
				prev2 = id

		else:

			print id
			raise Exception

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:

	bam2fastq(optH['-i'], optH['-o'])
