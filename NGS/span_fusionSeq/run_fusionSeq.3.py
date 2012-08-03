#!/usr/bin/python

import sys, os, re, getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:t',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH):

	print 'Usage: run_fusionSeq.3.py -i [input file dir]'
	sys.exit(0)

inputDirN = optH['-i']

inputFileNL = os.listdir(inputDirN)
inputFileNL = filter(lambda x: '1.gfr' not in x and 'confidence.gfr' not in x, filter(lambda x: re.match('.*\.gfr', x),inputFileNL))

print 'Files: %s' % inputFileNL

sampNL = list(set([re.match('(.*)\.gfr',inputFileN).group(1) for inputFileN in inputFileNL]))

sampNL.sort()

print 'Samples: %s' % sampNL

for sampN in sampNL:

	if '-t' in optH:

		print 'rm -f %s/%s.confidence.gfr %s/%s.fusionSeq.3.log' % (inputDirN,sampN, inputDirN,sampN)

		print 'cd %s; gfrConfidenceValues %s < %s/%s.gfr > %s/%s.confidence.gfr 2> %s/%s.fusionSeq.3.log' % \
			(inputDirN, sampN, inputDirN,sampN, inputDirN,sampN, inputDirN,sampN)
	else:

		os.system('rm -f %s/%s.confidence.gfr %s/%s.fusionSeq.3.log' % (inputDirN,sampN, inputDirN,sampN))

		os.system('cd %s; gfrConfidenceValues %s < %s/%s.gfr > %s/%s.confidence.gfr 2> %s/%s.fusionSeq.3.log' % \
			(inputDirN, sampN, inputDirN,sampN, inputDirN,sampN, inputDirN,sampN))
