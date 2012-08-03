#!/usr/bin/python

import sys, os, re, getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:t',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH):

	print 'Usage: run_sam2mrf.py -i [input file dir]'
	sys.exit(0)

inputDirN = optH['-i']

inputFileNL = os.listdir(inputDirN)
inputFileNL = filter(lambda x: re.match('.*\.sorted\.sam', x),inputFileNL)

print 'Files: %s' % inputFileNL

sampNL = list(set([re.match('(.*)\.sorted\.sam',inputFileN).group(1) for inputFileN in inputFileNL]))

sampNL.sort()

print 'Samples: %s' % sampNL

for sampN in sampNL:

	if '-t' in optH:

		print 'rm -f %s/%s.mrf %s/%s.sam2mrf.log' % (inputDirN,sampN, inputDirN,sampN)

		print 'echo "/home/tools/RSEQtools-0.6/sam2mrf < %s/%s.sorted.sam > %s/%s.mrf 2> %s/%s.sam2mrf.log" | qsub -l walltime=99:99:99:99 -N %s -o %s/%s.qlog -j oe' % \
			(inputDirN,sampN, inputDirN,sampN, inputDirN,sampN, sampN, inputDirN,sampN)
	else:

		os.system('rm -f %s/%s.mrf %s/%s.sam2mrf.log' % (inputDirN,sampN, inputDirN,sampN))

		os.system('echo "/home/tools/RSEQtools-0.6/sam2mrf < %s/%s.sorted.sam > %s/%s.mrf 2> %s/%s.sam2mrf.log" | qsub -l walltime=99:99:99:99 -N %s -o %s/%s.qlog -j oe' % \
			(inputDirN,sampN, inputDirN,sampN, inputDirN,sampN, sampN, inputDirN,sampN))
