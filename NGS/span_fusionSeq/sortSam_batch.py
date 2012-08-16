#!/usr/bin/python

import sys, os, re, getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH):

	print 'Usage: sortSam_batch.py -i [input file dir]'
	sys.exit(0)

inputDirN = optH['-i']

inputFileNL = os.listdir(inputDirN)
inputFileNL = filter(lambda x: 'sorted' not in x, filter(lambda x: re.match('.*\.sam', x),inputFileNL))

print 'Files: %s' % inputFileNL

sampNL = list(set([re.match('(.*)\.sam',inputFileN).group(1) for inputFileN in inputFileNL]))

sampNL.sort()

print 'Samples: %s' % sampNL

for sampN in sampNL:

	print 'Running %s' % sampN

	os.system('echo "/home/jinkuk/Codes/NGS/span_fusionSeq/sortSam.py %s/%s.sam > %s/%s.sorted.sam" | qsub -l walltime=99:99:99:99 -N %s -o %s/%s.qlog -j oe' % \
		(inputDirN,sampN, inputDirN,sampN, sampN, inputDirN,sampN))
