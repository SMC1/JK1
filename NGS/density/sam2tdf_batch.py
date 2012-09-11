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

#	if sampN[:-5] in ['G17663.TCGA-19-2619-01A-01R-1850-01.2','G17814.TCGA-06-5411-01A-01R-1849-01.4','G17212.TCGA-06-0129-01A-01R-1849-01.2','G17188.TCGA-02-0047-01A-01R-1849-01.2','G17188.TCGA-02-0047-01A-01R-1849-01.2','G17507.TCGA-28-1747-01C-01R-1850-01.2','G17511.TCGA-06-2565-01A-01R-1849-01.2','G17511.TCGA-06-2565-01A-01R-1849-01.2','G17511.TCGA-06-2565-01A-01R-1849-01.2','G17650.TCGA-28-2513-01A-01R-1850-01.2','G17790.TCGA-06-5856-01A-01R-1849-01.4','G17797.TCGA-28-5207-01A-01R-1850-01.4','G17807.TCGA-28-5209-01A-01R-1850-01.4']:
#		continue

	if '-p' in optH:

		os.system('echo "samtools view -S -b %s/%s.sorted.sam | bamToBed -i stdin | sort -k1,1 | \
			genomeCoverageBed -bg -i stdin -g /data1/Sequence/ucsc_hg19/chromsizes_hg19.txt > %s/%s.bedgraph; \
			igvtools toTDF -z 4 %s/%s.bedgraph %s/%s_z5.tdf hg19" | qsub -N %s -o %s/%s.qlog -j oe' % \
			(inputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))

	else:

		print sampN

		os.system('(samtools view -S -b %s/%s.sorted.sam | bamToBed -i stdin | sort -k1,1 | \
			genomeCoverageBed -bg -i stdin -g /data1/Sequence/ucsc_hg19/chromsizes_hg19.txt > %s/%s.bedgraph; \
			igvtools toTDF -z 4 %s/%s.bedgraph %s/%s_z5.tdf hg19) 2> %s/%s.qlog' % \
			(inputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN))
