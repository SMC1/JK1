#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mygenome


def main(inputDirN, outputDirN, pbs=False, assemCode='hg19'):

	assemblyH = {'hg18':'/data1/Sequence/ucsc_hg18/hg18.fa', 'hg19':'/data1/Sequence/ucsc_hg19/hg19.fa'}
	assemFN = assemblyH[assemCode] #mygenome.assemblyH[assemCode]

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('(.*)\.recal\.bam', x),inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.recal\.bam',inputFileN).group(1) for inputFileN in inputFileNL]))

	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

		if sampN not in ['NS08_567T','NS09_732T','NS08_567T_B','NS08_586T_B']:
			continue

		if pbs:

			print sampN

			os.system('echo "samtools mpileup -f %s %s/%s.recal.bam > %s/%s.pileup" | \
				qsub -N %s -o %s/%s.pileup.qlog -j oe' % \
				(assemFN, inputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))
		else:

			print sampN

			os.system('samtools mpileup -f %s %s/%s.recal.bam > %s/%s.pileup 2> %s/%s.pileup.qlog' % \
				(assemFN, inputDirN,sampN, outputDirN,sampN, outputDirN,sampN))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

optH = mybasic.parseParam(optL)

main('/data1/IRCR/exome_bam', '/data1/IRCR/exome_bam/mutation', True)
