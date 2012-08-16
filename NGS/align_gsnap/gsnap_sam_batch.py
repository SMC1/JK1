#!/usr/bin/python

import sys, os, re, getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

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

for sampN in sampNL[::-1]:

	if 'G17634.TCGA-19-2625-01A-01R-1850-01' in sampN:

		os.system('echo "/usr/local/bin/gsnap --db=hg19_nh --batch=4 --nthreads=1 -m 0 --query-unk-mismatch=1 --terminal-threshold=9 -y 0 -z 0 -Y 0 -Z 0 \
			--nofails --quality-protocol=%s --npath=1 -Q -A sam %s/%s.1.fastq %s/%s.2.fastq > %s/%s.sam" | qsub -l walltime=99:99:99:99 -N %s -o %s/%s.qlog -j oe' % \
			(qualType, inputDirN,sampN, inputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))
