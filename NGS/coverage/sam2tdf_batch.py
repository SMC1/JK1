#!/usr/bin/python

import sys, os, re, getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH):

	print 'Usage: sam2tdf_batch.py -i [input file dir]'
	sys.exit(0)

inputDirN = optH['-i']

if '-o' in optH:
	outputDirN = optH['-o']
else:
	outputDirN = inputDirN

inputFileNL = os.listdir(inputDirN)
inputFileNL = filter(lambda x: re.match('.*\.sorted\.sam', x),inputFileNL)

print 'Files: %s' % inputFileNL

sampNL = list(set([re.match('(.*)\.sorted\.sam',inputFileN).group(1) for inputFileN in inputFileNL]))

sampNL.sort()

print 'Samples: %s' % sampNL

for sampN in sampNL:

	if sampN[:-5] not in ['G17501.TCGA-27-2528-01A-01R-1850-01.2']:
		continue

	if '-p' in optH:

		os.system('echo "samtools view -S -b %s/%s.sorted.sam | bamToBed -i stdin | sort -k1,1 | \
			genomeCoverageBed -bg -i stdin -g /data1/Sequence/ucsc_hg19/chromsizes_hg19.txt > %s/%s.bedgraph; \
			igvtools toTDF -z 4 %s/%s.bedgraph %s/%s_z4.tdf hg19" | qsub -N %s -o %s/%s.qlog -j oe' % \
			(inputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))

	else:

		print sampN

		os.system('(samtools view -S -b %s/%s.sorted.sam | bamToBed -i stdin | sort -k1,1 | \
			genomeCoverageBed -bg -i stdin -g /data1/Sequence/ucsc_hg19/chromsizes_hg19.txt > %s/%s.bedgraph; \
			igvtools toTDF -z 4 %s/%s.bedgraph %s/%s_z4.tdf hg19) 2> %s/%s.qlog' % \
			(inputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN))
