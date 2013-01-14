#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def bam2tdf_batch(inputDirN,outputDirN,assembly='hg19',z=4):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: not 'sort' in x, filter(lambda x: re.match('.*\.bam', x),inputFileNL))

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.bam',inputFileN).group(1) for inputFileN in inputFileNL]))

	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

		if sampN not in ['C484.TCGA-06-0879-01A-01D-1492-08.4','C484.TCGA-06-2569-01A-01D-1494-08.5'] + \
				['C484.TCGA-74-6573-01A-12D-1845-08.2','C484.TCGA-06-0173-01A-01D-1491-08.5','C282.TCGA-12-1092-01B-01W-0611-08.2','C484.TCGA-06-0122-01A-01D-1490-08.5',\
				'C484.TCGA-06-0214-01A-02D-1491-08.5','C282.TCGA-27-1836-01A-01W-0837-08.1','C484.TCGA-19-1790-01B-01D-1353-08.2','C484.TCGA-32-4211-01A-01D-1353-08.2',\
				'C282.TCGA-32-1982-01A-01W-0837-08.1','TCGA-06-0878-01A-01W-0424-08_IlluminaGA-DNASeq_capture','TCGA-19-1786-01A-01W-0643-08_IlluminaGA-DNASeq_capture',\
				'C484.TCGA-06-0169-01A-01D-1490-08.4','C484.TCGA-06-2570-01A-01D-1495-08.5']:
			continue

		if '-p' in optH:

			os.system('echo "genomeCoverageBed -bg -ibam %s/%s.bam -g /data1/Sequence/ucsc_%s/%s.chrom.sizes > %s/%s.bedgraph; \
				igvtools toTDF -z %s %s/%s.bedgraph %s/%s.tdf %s" | qsub -N %s -o %s/%s.qlog -j oe' % \
				(inputDirN,sampN, assembly, assembly, outputDirN,sampN, z, outputDirN,sampN, outputDirN,sampN, assembly, sampN, outputDirN,sampN))

		else:

			os.system('(genomeCoverageBed -bg -ibam %s/%s.bam -g /data1/Sequence/ucsc_%s/%s.chrom.sizes > %s/%s.bedgraph; \
				igvtools toTDF -z %s %s/%s.bedgraph %s/%s.tdf %s) 2> %s/%s.qlog' % \
				(inputDirN,sampN, assembly, assembly, outputDirN,sampN, z, outputDirN,sampN, outputDirN,sampN, assembly, outputDirN,sampN))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

optH = mybasic.parseParam(optL)

inputDirN = optH['-i']

if '-o' in optH:
	outputDirN = optH['-o']
else:
	outputDirN = inputDirN

bam2tdf_batch(inputDirN,outputDirN,'hg18',3)
