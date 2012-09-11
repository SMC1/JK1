#!/usr/bin/python

import sys, os, re, getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH):

	print 'Usage: calMeta_batch.py -i (input file dir) [-p]'
	sys.exit(0)

inputDirN = optH['-i']

if '-o' in optH:
	outputDirN = optH['-o']
else:
	outputDirN = inputDirN

inputFileNL = os.listdir(inputDirN)
inputFileNL = filter(lambda x: re.match('.*\.mrf', x),inputFileNL)

print 'Files: %s' % inputFileNL

sampNL = list(set([re.match('(.*)\.mrf',inputFileN).group(1) for inputFileN in inputFileNL]))

sampNL.sort()

print 'Samples: %s' % sampNL

for sampN in sampNL:

	if sampN in ['G17189.TCGA-06-0132-01A-02R-1849-01.2_30nt','G17500.TCGA-27-1831-01A-01R-1850-01.2_30nt','G17501.TCGA-27-2528-01A-01R-1850-01.2_30nt','G17502.TCGA-14-0871-01A-01R-1849-01.2_30nt']:

		if '-p' in optH:

			os.system('echo "/home/jinkuk/Codes/NGS/span_fusionSeq/calMeta.py %s/%s.mrf > %s/%s.meta" | qsub -N %s -o %s/qlog/%s.meta.qlog -j oe' % \
				(inputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))

		else:

			print sampN

			os.system('/home/jinkuk/Codes/NGS/span_fusionSeq/calMeta.py %s/%s.mrf > %s/%s.meta 2> %s/qlog/%s.meta.qlog' % \
				(inputDirN,sampN, outputDirN,sampN, outputDirN,sampN))
