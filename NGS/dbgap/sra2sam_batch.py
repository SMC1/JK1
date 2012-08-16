#!/usr/bin/python

import sys, os, re, getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH and '-o' in optH):

	print 'Usage: sra2fastq_batch.py -i [input file dir]  -o [output file dir]'
	sys.exit(0)

inputDirN = optH['-i']
outputDirN = optH['-o']

qualType = 'sanger'

inputFileNL = os.listdir(inputDirN)
inputFileNL = filter(lambda x: re.match('.*\.sra$', x),inputFileNL)

print 'Files: %s' % inputFileNL

for inputFileN in inputFileNL:

	os.system('/home/tools/sratoolkit.2.1.9-centos_linux64/fastq-dump --split-3 -O %s %s/%s' % (outputDirN,inputDirN,inputFileN))
