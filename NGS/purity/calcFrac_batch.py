#!/usr/bin/python

import sys, os, re, getopt
import mybasic

cnlohCutoff = 0.2 
lohCutoff = -0.5

def main(inSegDirN, inputDirN, outputDirN, pbs=False):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('.*_LOH_af.txt', x), inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)_LOH_af.txt',inputFileN).group(1) for inputFileN in inputFileNL]))
	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

		print sampN
		
		cmd = '~/JK1/NGS/purity/calcFrac.py -i %s/%s.seg -f %s/%s_LOH_af.txt -o %s/%s_frac.txt -c %s -l %s' % (inSegDirN, sampN, inputDirN,sampN, outputDirN,sampN, cnlohCutoff, lohCutoff)
		log = '%s/%s.frac.log' % (outputDirN,sampN)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))

		else:
			os.system('(%s) 2> %s' % (cmd, log))



if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

	main('/EQL1/NSL/CGH/seg/link','/EQL1/NSL/exome_bam/purity', '/EQL1/NSL/exome_bam/purity', False)
