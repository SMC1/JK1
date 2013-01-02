#!/usr/bin/python

import sys, os, re, getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH):

	print 'Usage: batch_bam2tdf.py -i [input file dir]'
	sys.exit(0)

inputDirN = optH['-i']

if '-o' in optH:
	outputDirN = optH['-o']
else:
	outputDirN = inputDirN

inputFileNL = os.listdir(inputDirN)
inputFileNL = filter(lambda x: not 'sort' in x, filter(lambda x: re.match('.*\.bam', x),inputFileNL))

print 'Files: %s' % inputFileNL

sampNL = list(set([re.match('(.*)\.bam',inputFileN).group(1) for inputFileN in inputFileNL]))

sampNL.sort()

print 'Samples: %s' % sampNL

for sampN in sampNL:

#	if sampN not in ['C484.TCGA-12-5299-01A-02D-1486-08.6']:
#		continue

	if '-p' in optH:

		os.system('echo "genomeCoverageBed -bg -ibam %s/%s.bam -g /data1/Sequence/ucsc_hg19/chromsizes_hg19.txt > %s/%s.bedgraph; \
			igvtools toTDF -z 4 %s/%s.bedgraph %s/%s.tdf hg19" | qsub -N %s -o %s/%s.qlog -j oe' % \
			(inputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))

	else:

		print '(genomeCoverageBed -bg -ibam %s/%s.bam -g /data1/Sequence/ucsc_hg19/chromsizes_hg19.txt > %s/%s.bedgraph; \
			igvtools toTDF -z 4 %s/%s.bedgraph %s/%s.tdf hg19) 2> %s/%s.qlog' % \
			(inputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN)

		os.system('(genomeCoverageBed -bg -ibam %s/%s.bam -g /data1/Sequence/ucsc_hg19/chromsizes_hg19.txt > %s/%s.bedgraph; \
			igvtools toTDF -z 4 %s/%s.bedgraph %s/%s.tdf hg19) 2> %s/%s.qlog' % \
			(inputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN))
