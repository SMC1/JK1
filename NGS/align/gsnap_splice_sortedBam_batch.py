#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def align(inputDirN, outputDirN, memSize, pbs=False):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('.*\.fq\.gz', x),inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.[12]\.fq\.gz',inputFileN).group(1) for inputFileN in inputFileNL]))

	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

		if sampN in ['S647_RSq']:
			continue

		if pbs:

			print('%s' % sampN)

			os.system('echo "zcat %s/%s.1.fq.gz %s/%s.2.fq.gz | \
				/usr/local/bin/gsnap --db=hg19 --batch=5 --nthreads=40 --npath=1 -N 1 --nofails -Q -A sam --query-unk-mismatch=1 | \
				samtools view -Sb - | samtools sort -m %s - %s/%s.sorted" | qsub -N %s -o %s/%s.gsnap.log -j oe' % \
				(inputDirN,sampN, inputDirN,sampN, memSize, outputDirN,sampN, sampN, outputDirN,sampN))

		else:

			print('%s' % sampN)

			os.system('(zcat %s/%s.1.fq.gz %s/%s.2.fq.gz | \
				/usr/local/bin/gsnap --db=hg19 --batch=5 --nthreads=40 --npath=1 -N 1 --nofails -Q -A sam --query-unk-mismatch=1 | \
				samtools view -Sb - | samtools sort -m %s - %s/%s.sorted) 2> %s/%s.gsnap.log' % \
				(inputDirN,sampN, inputDirN,sampN, memSize, outputDirN,sampN, outputDirN,sampN))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

optH = mybasic.parseParam(optL)

#inputDirN = optH['-i']
#outputDirN = optH['-o']
#align(inputDirN, outputDirN)

align('/EQL1/NSL/RNASeq/fastq/link41', '/EQL1/NSL/RNASeq/align/splice_bam', 40000000000, True)
