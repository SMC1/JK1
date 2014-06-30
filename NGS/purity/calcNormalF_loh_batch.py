#!/usr/bin/python

import sys, os, re, getopt
import mybasic

def main(inAFDirN, inputDirN, outputDirN, pbs=False):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('.*\.loh_cn\.txt', x), inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.loh_cn\.txt',inputFileN).group(1) for inputFileN in inputFileNL]))
	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

		print sampN
		
		cmd = '~/JK1/NGS/purity/calcNormalF_loh.py -i %s/%s.dbaf.txt -l %s/%s.loh_cn.txt -o %s/%s.nFrac_all.txt' % (inAFDirN, sampN, inputDirN,sampN, outputDirN,sampN)
		log = '%s/%s.nfrac_all.log' % (outputDirN,sampN)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))

		else:
			os.system('(%s) 2> %s' % (cmd, log))



if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

	main('/EQL1/NSL/exome_bam/purity','/EQL1/NSL/exome_bam/purity', '/EQL1/NSL/exome_bam/purity', False)
