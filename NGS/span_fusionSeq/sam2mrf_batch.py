#!/usr/bin/python

import sys, os, re, getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

optH = mybasic.parseParam(optL)

if not '-i' in optH:

	print 'Usage: sam2mrf_batch.py -i [input file dir] [-o (output file dir)] [-p]'
	sys.exit(0)

if '-p' in optH:
	pbs = True
else:
	pbs = False

inputDirN = optH['-i']

if '-o' in optH:
	outputDirN = optH['-o']
else:
	outputDirN = inputDirN

inputFileNL = os.listdir(inputDirN)
inputFileNL = filter(lambda x: re.match('.*\.sorted\.sam', x),inputFileNL)

print 'Files: %s' % inputFileNL

sampNL = list(set([re.match('(.*)\.sorted\.sam',inputFileN).group(1) for inputFileN in inputFileNL]))

sampNL.sort()

print 'Samples: %s' % sampNL

for sampN in sampNL:

#	if sampN in ['G17189.TCGA-06-0132-01A-02R-1849-01.2_30nt','G17500.TCGA-27-1831-01A-01R-1850-01.2_30nt','G17501.TCGA-27-2528-01A-01R-1850-01.2_30nt','G17502.TCGA-14-0871-01A-01R-1849-01.2_30nt']:

	if pbs:
		os.system('echo "/home/tools/RSEQtools-0.6/sam2mrf < %s/%s.sorted.sam > %s/%s.mrf" | qsub -N %s -o %s/qlog/%s.mrf.qlog -j oe' % \
			(inputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))
	else:
		print '/home/tools/RSEQtools-0.6/sam2mrf < %s/%s.sorted.sam > %s/%s.mrf' % (inputDirN,sampN, outputDirN,sampN)
		os.system('/home/tools/RSEQtools-0.6/sam2mrf < %s/%s.sorted.sam > %s/%s.mrf' % (inputDirN,sampN, outputDirN,sampN))
