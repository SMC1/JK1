#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mysetting

#minCover = 3
#minMutReads = 2
#minFreq = 0.01

def main(inputDirN, outputDirN, pbs=False, minCover=3, minMutReads=2, minFreq = 0.01):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('.*chr.*\.pileup_proc', x),inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)_chr.*\.pileup_proc',inputFileN).group(1) for inputFileN in inputFileNL]))
	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

#		if sampN not in ['NS09_671T']:
#			continue

		print sampN
		cmd = '%s/NGS/mutation/mutScan.py -s %s -i %s -o %s/%s.mutscan -c %s -m %s -f %s' % (mysetting.SRC_HOME, sampN, inputDirN, outputDirN,sampN, minCover, minMutReads, minFreq)
		log = '%s/%s.mutscan.log' % (outputDirN,sampN)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))

		else:
			os.system('(%s) 2> %s' % (cmd, log))



if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

	main('/EQL1/NSL/exome_bam/mutation/pileup_proc', '/EQL1/NSL/exome_bam/mutation/mutscan', True)
	#main('/Z/NSL/RNASeq/align/splice/gatk_test/pileup_proc', '/Z/NSL/RNASeq/align/splice/gatk_test/mutation', False)
