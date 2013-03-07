#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def main(inputDirN, outputDirN):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = set(filter(lambda x: re.match('(.*)\.snp', x),inputFileNL))
	exNL = set(filter(lambda x: re.match('(.*)\.snp.\qlog', x),inputFileNL))
	inputFileNL = list(inputFileNL - exNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.snp',inputFileN).group(1) for inputFileN in inputFileNL]))

	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

#		if sampN not in ['NS09_671T']:
#			continue
#
#		if pbs:
#
#			print sampN
#
#			os.system('echo "samtools mpileup -f %s %s/%s.realign.bam > %s/%s.pileup" | \
#				qsub -N %s -o %s/%s.pileup.qlog -j oe' % \
#				(assemFN, inputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))
#		else:
#
		print sampN

		os.system('tail -q -n +2 %s/%s.snp > %s/%s_noheader.snp' % \
			(inputDirN,sampN, outputDirN,sampN))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

main('/data1/IRCR/exome_bam/mutation', '/data1/IRCR/exome_bam/mutation')
