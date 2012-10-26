#!/usr/bin/python

import sys, os, re, getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH):

	print 'Usage: fusionSeq.1.py -i (input file dir) [-o (output file dir)]'
	sys.exit(0)

inputDirN = optH['-i']

if '-o' in optH:
	outputDirN = optH['-o']
else:
	outputDirN = inputDirN

inputFileNL = os.listdir(inputDirN)
#inputFileNL = filter(lambda x: re.match('.*\.mrf', x),inputFileNL)
inputFileNL = filter(lambda x: re.match('.*\.sorted\.sam', x),inputFileNL)

print 'Files: %s' % inputFileNL

#sampNL = list(set([re.match('(.*)\.mrf',inputFileN).group(1) for inputFileN in inputFileNL]))
sampNL = list(set([re.match('(.*)\.sorted\.sam',inputFileN).group(1) for inputFileN in inputFileNL]))

sampNL.sort()

print 'Samples: %s' % sampNL

for sampN in sampNL:

	if '-p' in optH:

		os.system('echo "geneFusions %s 4 < %s/%s.mrf | gfrClassify > %s/%s.1.gfr" | qsub -N %s -o %s/qlog/%s.1.qlog -j oe' % \
			(sampN, inputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))

	else:

		print '(geneFusions %s 4 < %s/%s.mrf | gfrClassify > %s/%s.1.gfr) 2> %s/qlog/%s.1.qlog' % \
			(sampN, inputDirN,sampN, outputDirN,sampN, outputDirN,sampN)

		os.system('(geneFusions %s 4 < %s/%s.mrf | gfrClassify > %s/%s.1.gfr) 2> %s/qlog/%s.1.qlog' % \
			(sampN, inputDirN,sampN, outputDirN,sampN, outputDirN,sampN))
