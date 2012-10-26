#!/usr/bin/python

import sys, os, re

if len(sys.argv) < 2:

	print 'Usage: fastx_stats_run.py [input file directory] [input file regular expression pattern; optional]'
	sys.exit(0)

inputDirName = sys.argv[1]

if len(sys.argv) < 3:
	inputFilePattern = '.*'
else:
	inputFilePattern = sys.argv[2]

inputFileNameL = os.listdir(inputDirName)
inputFileNameL = filter(lambda x: re.match(inputFilePattern,x), inputFileNameL)

print 'Files: %s' % inputFileNameL

try:
	os.mkdir('%s/fastx' % inputDirName)
except:
	pass

for inputFileName in inputFileNameL:
	print 'fastx_quality_stats -Q33 -i %s/%s -o %s/fastx/%s_quality.txt &' % (inputDirName,inputFileName, inputDirName,os.path.splitext(inputFileName)[0])
	#print 'fastx_quality_stats -Q33 -i %s/%s -o %s/fastx/%s_quality.txt &' % (inputDirName,inputFileName, inputDirName,os.path.splitext(inputFileName)[0])
	os.system('fastx_quality_stats -Q33 -i %s/%s -o %s/fastx/%s_quality.txt &' % (inputDirName,inputFileName, inputDirName,os.path.splitext(inputFileName)[0]))
