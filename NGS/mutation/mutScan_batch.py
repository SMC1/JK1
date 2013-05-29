#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mygenome

minCover = 3
minMutReads = 2
minFreq = 0.01

def main(inputDirN, outputDirN, pbs=False):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('.*chr.*\.pileup_proc', x),inputFileNL)

	sampNL = list(set([re.match('(.*)_chr.*\.pileup_proc',inputFileN).group(1) for inputFileN in inputFileNL]))
	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

#		if sampN not in ['NS09_671T']:
#			continue

		if pbs:

			print sampN

			os.system('echo "~/JK1/NGS/mutation/mutScan.py -s %s -i %s -o %s/%s.mutscan -c %s -m %s -f %s" | \
				qsub -N %s -o %s/%s.mutscan.log -j oe' % \
				(sampN, inputDirN, outputDirN,sampN,minCover,minMutReads,minFreq, sampN, outputDirN,sampN))
		else:

			print sampN

			os.system('(~/JK1/NGS/mutation/mutScan.py -s %s -i %s -o %s/%s.mutscan -c %s -m %s -f %s) 2> %s/%s.mutscan.log' % \
				(sampN, inputDirN, outputDirN,sampN,minCover,minMutReads,minFreq, outputDirN,sampN))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

optH = mybasic.parseParam(optL)

#main('/EQL1/NSL/exome_bam/mutation/pileup_proc', '/EQL1/NSL/exome_bam/mutation/mutscan', True)
main('/Z/NSL/RNASeq/align/splice/gatk_test/pileup_proc', '/Z/NSL/RNASeq/align/splice/gatk_test/mutation', False)
