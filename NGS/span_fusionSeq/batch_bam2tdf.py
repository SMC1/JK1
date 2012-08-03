#!/usr/bin/python

import sys, os, re, getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:t',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH):

	print 'Usage: batch_bam2tdf.py -i [input file dir]'
	sys.exit(0)

inputDirN = optH['-i']

inputFileNL = os.listdir(inputDirN)
inputFileNL = filter(lambda x: not 'sort' in x, filter(lambda x: re.match('.*\.bam', x),inputFileNL))

print 'Files: %s' % inputFileNL

sampNL = list(set([re.match('(.*)\.bam',inputFileN).group(1) for inputFileN in inputFileNL]))

sampNL.sort()

print 'Samples: %s' % sampNL

for sampN in sampNL:

	if '-t' in optH:

		print 'rm -f %s/%s.bedgraph %s/%s.tdf' % (inputDirN,sampN, inputDirN,sampN)

		print 'echo "genomeCoverageBed -bg -ibam %s/%s.bam -g /data1/Sequence/ucsc_hg19/chromsizes_hg19.txt > %s/%s.bedgraph; \
			igvtools toTDF %s/%s.bedgraph %s/%s.tdf hg19" | qsub -l walltime=99:99:99:99 -N %s -o %s/%s.qlog -j oe' % \
			(inputDirN,sampN, inputDirN,sampN, inputDirN,sampN, inputDirN,sampN, sampN, inputDirN,sampN)
	else:

		os.system('rm -f %s/%s.bedgraph %s/%s.tdf' % (inputDirN,sampN, inputDirN,sampN))

		os.system('echo "genomeCoverageBed -bg -ibam %s/%s.bam -g /data1/Sequence/ucsc_hg19/chromsizes_hg19.txt > %s/%s.bedgraph; \
			igvtools toTDF %s/%s.bedgraph %s/%s.tdf hg19" | qsub -l walltime=99:99:99:99 -N %s -o %s/%s.qlog -j oe' % \
			(inputDirN,sampN, inputDirN,sampN, inputDirN,sampN, inputDirN,sampN, sampN, inputDirN,sampN))
