#!/usr/bin/python

import sys, os, re, getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH):

	print 'Usage: fusionSeq.3.py -i (input file dir)'
	sys.exit(0)

inputDirN = optH['-i']

inputFileNL = os.listdir(inputDirN)
inputFileNL = filter(lambda x: '1.gfr' not in x and 'confidence.gfr' not in x, filter(lambda x: re.match('.*\.gfr', x),inputFileNL))

print 'Files: %s' % inputFileNL

sampNL = list(set([re.match('(.*)\.gfr',inputFileN).group(1) for inputFileN in inputFileNL]))

sampNL.sort()

print 'Samples: %s' % sampNL

# (sampN).meta should be available in the directory

for sampN in sampNL:

	print sampN

	os.system('cd %s; gfrConfidenceValues %s < %s/%s.gfr > %s/%s.confidence.gfr 2> %s/qlog/%s.3.qlog' % \
		(inputDirN, sampN, inputDirN,sampN, inputDirN,sampN, inputDirN,sampN))
