#!/usr/bin/python

import sys, os, re, getopt
import mybasic

def main(inDir, outDir, pbs=False):

	inFileNL = os.listdir(inDir)
	inFileNL = filter(lambda x: re.match('(.*)\.nFrac_all\.txt', x), inFileNL)

	print 'Files: %s' % inFileNL

	sampNL = list(set([re.match('(.*)\.nFrac_all\.txt', inFileN).group(1) for inFileN in inFileNL]))
	sampNL.sort()

	print 'Samples: %s' % sampNL, len(sampNL)

	for sampN in sampNL:

		print sampN

		iprefix = '%s/%s' % (inDir,sampN)
		oprefix = '%s/%s' % (outDir,sampN)
		cmd = 'Rscript ~/JK1/NGS/purity/peakFrac.r %s.nFrac_all.txt %s %s' % (iprefix, outDir, sampN)
		log = '%s.tfrac.log' % (oprefix)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))

		else:
			os.system('(%s) &> %s' % (cmd, log))		


if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

	optH = mybasic.parseParam(optL)

	main('/EQL1/NSL/exome_bam/purity','/EQL1/NSL/exome_bam/purity', False)
