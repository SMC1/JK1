#!/usr/bin/python

import sys, os, re, getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:t',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH):

	print 'Usage: run_calMeta.py -i [input file dir]'
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

		print 'rm -f %s/%s.meta %s/%s.calMeta.log' % (inputDirN,sampN, inputDirN,sampN)

		print 'echo "/home/jinkuk/Codes/NGS/fusionSeq/calMeta.py %s/%s.mrf > %s/%s.meta 2> %s/%s.calMeta.log" | qsub -l walltime=99:99:99:99 -N %s -o %s/%s.qlog -j oe' % \
			(inputDirN,sampN, inputDirN,sampN, inputDirN,sampN, sampN, inputDirN,sampN)
	else:

		os.system('rm -f %s/%s.meta %s/%s.calMeta.log' % (inputDirN,sampN, inputDirN,sampN))

		os.system('echo "/home/jinkuk/Codes/NGS/fusionSeq/calMeta.py %s/%s.mrf > %s/%s.meta 2> %s/%s.calMeta.log" | qsub -l walltime=99:99:99:99 -N %s -o %s/%s.qlog -j oe' % \
			(inputDirN,sampN, inputDirN,sampN, inputDirN,sampN, sampN, inputDirN,sampN))
