#!/usr/bin/python

import sys, os, re, getopt
import mybasic

def main(inDir, outDir, refFlatPath, pbs=False):

	inFileNL = os.listdir(inDir)
	inFileNL = filter(lambda x: re.match('(.*)\.bed', x), inFileNL)

	print 'Files: %s' % inFileNL

	sampNL = list(set([re.match('(.*)\.bed', inFileN).group(1) for inFileN in inFileNL]))
	sampNL.sort()

	print 'Samples: %s' % sampNL, len(sampNL)

	for sampN in sampNL:

#		if sampN not in ['G17819.TCGA-26-1442-01A-01R-1850-01.4_30nt']:
#			continue
		
		print sampN

		if pbs:

			os.system('echo "Rscript /home/heejin/JK1/NGS/expression/degSeq.R %s/%s.bed %s/%s.rpkm %s" | qsub -N %s -o %s/%s.degSeq.qlog -j oe' \
			% (inDir,sampN, outDir,sampN, refFlatPath, sampN, outDir,sampN))

		else:
		
			os.system('(Rscript /home/heejin/JK1/NGS/expression/degSeq.R %s/%s.bed %s/%s.rpkm %s) 2> %s/%s.degSeq.qlog' \
			% (inDir,sampN, outDir,sampN, refFlatPath, outDir,sampN))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

optH = mybasic.parseParam(optL)

main('/EQL1/NSL/RNASeq/coverage', '/EQL1/NSL/RNASeq/expression', '/data1/Sequence/ucsc_hg19/annot/refFlat.txt',True)
