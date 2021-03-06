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

	#if sampN in ['G17189.TCGA-06-0132-01A-02R-1849-01.2_30nt','G17500.TCGA-27-1831-01A-01R-1850-01.2_30nt','G17501.TCGA-27-2528-01A-01R-1850-01.2_30nt','G17502.TCGA-14-0871-01A-01R-1849-01.2_30nt']:

	print 'Running %s' % sampN

#	os.system('/home/jinkuk/Codes/NGS/span_fusionSeq/sortSam.py %s/%s.sam > %s/%s.sorted.sam' % \
#		(inputDirN,sampN, inputDirN,sampN))

	os.system('echo "/home/jinkuk/Codes/NGS/span_fusionSeq/sortSam.py %s/%s.sam > %s/%s.sorted.sam" | qsub -N %s -o %s/qlog/%s.sort.qlog -j oe' % \
		(inputDirN,sampN, inputDirN,sampN, sampN, inputDirN,sampN))
