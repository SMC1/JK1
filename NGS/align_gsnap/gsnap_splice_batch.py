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

for sampN in sampNL:

	#	if sampN in ['G17506.TCGA-27-1835-01A-01R-1850-01.2','G17807.TCGA-28-5209-01A-01R-1850-01.4','G17501.TCGA-27-2528-01A-01R-1850-01.2','G17496.TCGA-14-0817-01A-01R-1849-01.2','G17790.TCGA-06-5856-01A-01R-1849-01.4','G17469.TCGA-06-2557-01A-01R-1849-01.2','G17208.TCGA-06-0187-01A-01R-1849-01.2','G17216.TCGA-12-0618-01A-01R-1849-01.2','G17211.TCGA-06-0747-01A-01R-1849-01.2','G17471.TCGA-27-2519-01A-01R-1850-01.2']:
	#	if sampN in ['G17212.TCGA-06-0129-01A-01R-1849-01.2']:
	#	if sampN in ['G17494.TCGA-14-2554-01A-01R-1850-01.2','G17803.TCGA-76-4925-01A-01R-1850-01.4','G17791.TCGA-32-1980-01A-01R-1850-01.4','G17676.TCGA-41-2571-01A-01R-1850-01.2','G17796.TCGA-41-5651-01A-01R-1850-01.4']:

	if '-p' in optH:

		os.system('echo "cat %s/%s.1.fastq %s/%s.2.fastq | \
			/usr/local/bin/gsnap --db=hg19 --batch=5 --nthreads=6 --npath=1 -N 1 --use-splicing=refGene_knownGene_splicesites --nofails -Q \
			 --query-unk-mismatch=1 > %s/%s_splice.gsnap" | qsub -N %s -o %s/%s.qlog -j oe' % (inputDirN,sampN, inputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))

	else:

		print('%s' % sampN)

		os.system('(cat %s/%s.1.fastq %s/%s.2.fastq | \
			/usr/local/bin/gsnap --db=hg19 --batch=5 --nthreads=6 --npath=1 -N 1 --use-splicing=refGene_knownGene_splicesites --nofails -Q \
			--query-unk-mismatch=1 > %s/%s_splice.gsnap) 2> %s/%s.qlog' % (inputDirN,sampN, inputDirN,sampN, outputDirN,sampN, outputDirN,sampN))
