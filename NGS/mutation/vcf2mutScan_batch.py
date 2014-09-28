#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mygenome, mysetting

minCover = 3
minMutReads = 2
minFreq = 0.01

def main(inputDirN, outputDirN, pbs=False):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('(.*)\.vcf', x),inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.vcf',inputFileN).group(1) for inputFileN in inputFileNL]))
	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

#		if sampN not in ['NS09_671T']:
#			continue

		print sampN
		iprefix = '%s/%s' % (inputDirN,sampN)
		oprefix = '%s/%s' % (outputDirN,sampN)
		cmd = '%s/NGS/mutation/vcf2mutScan.py -s %s -i %s.vcf -o %s.mutscan -c %s -m %s -f %s' % (mysetting.SRC_HOME, sampN, iprefix, oprefix, minCover, minMutReads, minFreq)
		log = '%s.mutscan.log' % (oprefix)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))

		else:
			os.system('(%s) 2> %s' % (cmd, log))


if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

	main('/EQL1/NSL/RNASeq/align/splice_Z/gatk_test', '/EQL1/NSL/RNASeq/align/splice_Z/gatk_test', False)
