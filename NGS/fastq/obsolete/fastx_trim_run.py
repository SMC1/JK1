#!/usr/bin/python

import sys, os, re, getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:e:l:t',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH and '-l' in optH):

	print 'Usage: fastx_trim_run.py -i [input file directory]  -l [number of nucleotides from 5p] -e [input file regular expression pattern; optional]'
	sys.exit(0)

inputDirName = optH['-i']
numNt = optH['-l']

try:
	inputFilePattern = optH['-e']
except:
	inputFilePattern = '.*'

inputFileNameL = os.listdir(inputDirName)
inputFileNameL = filter(lambda x: re.match(inputFilePattern,x), inputFileNameL)

print 'Files: %s' % inputFileNameL

try:
	os.mkdir('%s/trim_%s' % (inputDirName,numNt))
except:
	pass

for inputFileName in inputFileNameL:

	if '-t' in optH:
		print 'fastx_trimmer -i %s/%s -o %s/trim_%s/%s_%snt.fastq -l %s -Q33' % (inputDirName,inputFileName, inputDirName,numNt,os.path.splitext(inputFileName)[0],numNt,numNt)
	else:
		os.system('fastx_trimmer -i %s/%s -o %s/trim_%s/%s_%snt.fastq -l %s -Q33' % (inputDirName,inputFileName, inputDirName,numNt,os.path.splitext(inputFileName)[0],numNt,numNt))
