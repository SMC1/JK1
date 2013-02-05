#!/usr/bin/python

import sys, os, re, getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH and '-o' in optH):

	print 'Usage: gsnap_sam_batch.py -i [input file dir]  -o [output file dir]'
	sys.exit(0)

inputDirN = optH['-i']
outputDirN = optH['-o']

qualType = 'sanger'

inputFileNL = os.listdir(inputDirN)
inputFileNL = filter(lambda x: re.match('.*\.fastq', x),inputFileNL)

print 'Files: %s' % inputFileNL

sampNL = list(set([re.match('(.*)\.[12]\.fastq',inputFileN).group(1) for inputFileN in inputFileNL]))

sampNL.sort()

print 'Samples: %s' % sampNL

for sampN in sampNL[:1]:

#	if not sampN in ['G17189.TCGA-06-0132-01A-02R-1849-01.2_30nt','G17500.TCGA-27-1831-01A-01R-1850-01.2_30nt','G17501.TCGA-27-2528-01A-01R-1850-01.2_30nt','G17502.TCGA-14-0871-01A-01R-1849-01.2_30nt']:

	if '-p' in optH:

		os.system('echo "/usr/local/bin/gsnap --db=hg19_nh --batch=5 --nthreads=5 -m 0 --query-unk-mismatch=1 --terminal-threshold=9 -y 0 -z 0 -Y 0 -Z 0 \
			--nofails --quality-protocol=%s --npath=1 -Q -A sam %s/%s.1.fastq %s/%s.2.fastq > %s/%s.sam" | qsub -N %s -o %s/qlog/%s.gsnap.qlog -j oe' % \
			(qualType, inputDirN,sampN, inputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))

	else:

		print sampN

		os.system('(/usr/local/bin/gsnap --db=hg19_nh --batch=5 --nthreads=30 -m 0 --query-unk-mismatch=1 --terminal-threshold=9 -y 0 -z 0 -Y 0 -Z 0 \
			--nofails --quality-protocol=%s --npath=1 -Q -A sam %s/%s.1.fastq %s/%s.2.fastq > %s/%s.sam) 2> %s/%s.gsnap.qlog' % \
			(qualType, inputDirN,sampN, inputDirN,sampN, outputDirN,sampN, outputDirN,sampN))
