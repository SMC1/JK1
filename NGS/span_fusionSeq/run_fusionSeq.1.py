#!/usr/bin/python

import sys, os, re, getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:t',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH):

	print 'Usage: run_fusionSeq.1.py -i [input file dir]'
	sys.exit(0)

inputDirN = optH['-i']

inputFileNL = os.listdir(inputDirN)
inputFileNL = filter(lambda x: re.match('.*\.mrf', x),inputFileNL)

print 'Files: %s' % inputFileNL

sampNL = list(set([re.match('(.*)\.mrf',inputFileN).group(1) for inputFileN in inputFileNL]))

sampNL.sort()

print 'Samples: %s' % sampNL

for sampN in sampNL:

	if '-t' in optH:

		print 'rm -f %s/%s.1.gfr %s/%s.fusionSeq.1.log' % (inputDirN,sampN, inputDirN,sampN)

		print 'echo "geneFusions %s 4 < %s/%s.mrf | gfrClassify > %s/%s.1.gfr" | qsub -l walltime=99:99:99:99 -N %s -o %s/%s.fusionSeq.1.log -j oe' % \
			(sampN, inputDirN,sampN, inputDirN,sampN, sampN, inputDirN,sampN)
	else:

		os.system('rm -f %s/%s.1.gfr %s/%s.fusionSeq.1.log' % (inputDirN,sampN, inputDirN,sampN))

		os.system('echo "geneFusions %s 4 < %s/%s.mrf | gfrClassify > %s/%s.1.gfr" | qsub -l walltime=99:99:99:99 -N %s -o %s/%s.fusionSeq.1.log -j oe' % \
			(sampN, inputDirN,sampN, inputDirN,sampN, sampN, inputDirN,sampN))
