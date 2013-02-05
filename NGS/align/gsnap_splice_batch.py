#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def align(inputDirN, outputDirN):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('.*\.fq\.gz', x),inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.[12]\.fq\.gz',inputFileN).group(1) for inputFileN in inputFileNL]))

	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

	#	if not sampN in ['G17678.TCGA-06-5417-01A-01R-1849-01.2']:
	#		continue

		if '-p' in optH:

			print('%s' % sampN)

			os.system('echo "zcat %s/%s.1.fq.gz %s/%s.2.fq.gz | \
				/usr/local/bin/gsnap --db=hg19 --batch=5 --nthreads=6 --npath=1 -N 1 --use-splicing=refGene_knownGene_splicesites --nofails -Q \
				 --query-unk-mismatch=1 > %s/%s_splice.gsnap" | qsub -N %s -o %s/%s.gsnap.qlog -j oe' % (inputDirN,sampN, inputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))

		else:

			print('%s' % sampN)

			os.system('(zcat %s/%s.1.fq.gz %s/%s.2.fq.gz | \
				/usr/local/bin/gsnap --db=hg19 --batch=5 --nthreads=6 --npath=1 -N 1 --use-splicing=refGene_knownGene_splicesites --nofails -Q \
				--query-unk-mismatch=1 > %s/%s_splice.gsnap) 2> %s/%s.gsnap.qlog' % (inputDirN,sampN, inputDirN,sampN, outputDirN,sampN, outputDirN,sampN))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

optH = mybasic.parseParam(optL)

inputDirN = optH['-i']
outputDirN = optH['-o']

align(inputDirN, outputDirN)
