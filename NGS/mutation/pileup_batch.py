#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mygenome


def main(inputDirN, outputDirN, pbs=False, assemCode='hg19'):

	assemFN = mygenome.assemblyH[assemCode]

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('(.*)\.sorted\.bam', x),inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.sorted\.bam',inputFileN).group(1) for inputFileN in inputFileNL]))

	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

#		if sampN not in ['NS09_671T']:
#			continue

		if pbs:

			print sampN

			os.system('echo "samtools mpileup -f %s %s/%s.sorted.bam > %s/%s.pileup" | \
				qsub -N %s -o %s/%s.bwa.qlog -j oe' % \
				(assemFN, inputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))
		else:

			print sampN

			os.system('samtools mpileup -f %s %s/%s.sorted.bam > %s/%s.pileup 2> %s/%s.pileup.qlog' % \
				(assemFN, inputDirN,sampN, outputDirN,sampN, outputDirN,sampN))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

optH = mybasic.parseParam(optL)

main('/EQL1/NSL/Exome/bwa', '/EQL1/NSL/Exome/mutation', True)
