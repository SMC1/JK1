#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def bam2tdf_batch(inputDirN,outputDirN,assembly='hg19'):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: not 'sort' in x, filter(lambda x: re.match('.*\.bam', x),inputFileNL))

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.bam',inputFileN).group(1) for inputFileN in inputFileNL]))

	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL[:1]:

	#	if sampN not in ['C484.TCGA-12-5299-01A-02D-1486-08.6']:
	#		continue

		if '-p' in optH:

			os.system('echo "genomeCoverageBed -bg -ibam %s/%s.bam -g /data1/Sequence/ucsc_%s/%s.chrom.sizes > %s/%s.bedgraph; \
				igvtools toTDF -z 4 %s/%s.bedgraph %s/%s.tdf %s" | qsub -N %s -o %s/%s.qlog -j oe' % \
				(inputDirN,sampN, assembly, assembly, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, assembly, sampN, outputDirN,sampN))

		else:

			os.system('(genomeCoverageBed -bg -ibam %s/%s.bam -g /data1/Sequence/ucsc_%s/%s.chrom.sizes > %s/%s.bedgraph; \
				igvtools toTDF -z 4 %s/%s.bedgraph %s/%s.tdf %s) 2> %s/%s.qlog' % \
				(inputDirN,sampN, assembly, assembly, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, assembly, outputDirN,sampN))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

optH = mybasic.parseParam(optL)

inputDirN = optH['-i']

if '-o' in optH:
	outputDirN = optH['-o']
else:
	outputDirN = inputDirN

bam2tdf_batch(inputDirN,outputDirN,'hg18')
