#!/usr/bin/python

import sys, os, re, getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH and '-o' in optH):

	print 'Usage: gsnap_splice_batch.py -i [input file dir]  -o [output file dir] -p'
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

for sampN in sampNL[1:]:

	if '-p' in optH:

		os.system('echo "cat %s/%s.1.fastq %s/%s.2.fastq | \
			/usr/local/bin/gsnap --db=EGFR --batch=5 --nthreads=6 --npath=1 -N 0 --use-splicing=EGFR_mRNA_on_EGFR --nofails -Q \
			--query-unk-mismatch=1 > %s/%s_splice.gsnap" | qsub -N %s -o %s/%s.qlog -j oe' % (inputDirN,sampN, inputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))

	else:

		print('%s' % sampN)

		os.system('(cat %s/%s.1.fastq %s/%s.2.fastq | \
			/usr/local/bin/gsnap --db=EGFR --batch=5 --nthreads=6 --npath=1 -N 0 --use-splicing=EGFR_mRNA_on_EGFR --nofails -Q \
			--query-unk-mismatch=1 > %s/%s_splice.gsnap) 2> %s/%s.qlog' % (inputDirN,sampN, inputDirN,sampN, outputDirN,sampN, outputDirN,sampN))
