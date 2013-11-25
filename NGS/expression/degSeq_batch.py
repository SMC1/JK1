#!/usr/bin/python

import sys, os, re, getopt
import mybasic

def main(inDir, outDir, refFlatPath, pbs=False):

	inFileNL = os.listdir(inDir)
	inFileNL = filter(lambda x: re.match('(.*)\.sorted.bed', x), inFileNL)

	print 'Files: %s' % inFileNL

	sampNL = list(set([re.match('(.*)\.sorted.bed', inFileN).group(1) for inFileN in inFileNL]))
	sampNL.sort()

	print 'Samples: %s' % sampNL, len(sampNL)

	for sampN in sampNL:

#		if sampN not in ['G17819.TCGA-26-1442-01A-01R-1850-01.4_30nt']:
#			continue
		
		print sampN

		iprefix = '%s/%s' % (inDir,sampN)
		oprefix = '%s/%s' % (outDir,sampN)
		cmd = 'Rscript ~/JK1/NGS/expression/degSeq.R %s.sorted.bed %s.rpkm %s' % (iprefix, oprefix, refFlatPath)
		log = '%s.degSeq.qlog' % (oprefix)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))

		else:
			os.system('(%s) &> %s' % (cmd, log))		


if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

	optH = mybasic.parseParam(optL)

	main('/pipeline/test_rpkm/S436_T_SS','/pipeline/test_rpkm/S436_T_SS','/data1/Sequence/ucsc_hg19/annot/refFlat.txt',False)
	#main('/EQL1/NSL/RNASeq/coverage', '/EQL1/NSL/RNASeq/expression', '/data1/Sequence/ucsc_hg19/annot/refFlat.txt',True)
	#main('/EQL1/NSL/RNASeq/coverage/batch3', '/EQL1/NSL/RNASeq/expression/batch3', '/data1/Sequence/ucsc_hg19/annot/refFlat.txt',True)
