#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mygenome

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

		if pbs:

			print sampN

			os.system('echo "~/JK1/NGS/mutation/vcf2mutScan.py -s %s -i %s/%s.vcf -o %s/%s.mutscan -c %s -m %s -f %s" | \
				qsub -N %s -o %s/%s.mutscan.log -j oe' % \
				(sampN, inputDirN,sampN, outputDirN,sampN, minCover,minMutReads,minFreq, sampN, outputDirN,sampN))
		else:

			print sampN

			os.system('(~/JK1/NGS/mutation/vcf2mutScan.py -s %s -i %s/%s.vcf -o %s/%s.mutscan -c %s -m %s -f %s) 2> %s/%s.mutscan.log' % \
				(sampN, inputDirN,sampN, outputDirN,sampN, minCover,minMutReads,minFreq, outputDirN,sampN))


if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

	main('/EQL1/NSL/RNASeq/align/splice_Z/gatk_test', '/EQL1/NSL/RNASeq/align/splice_Z/gatk_test', False)
