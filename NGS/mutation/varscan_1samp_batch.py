#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mygenome


def main(inputDirN, outputDirN, pbs=False):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('(.*)\.pileup', x),inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.pileup',inputFileN).group(1) for inputFileN in inputFileNL]))

	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

#		if sampN not in ['NS09_671T']:
#			continue

		if pbs:

			print sampN

			os.system('echo "java -jar /home/tools/VarScan/VarScan.v2.3.3.jar mpileup2snp %s/%s.pileup > %s/%s.snp" | \
				qsub -N %s -o %s/%s.snp.qlog -j oe' % \
				(inputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))
		else:

			print sampN

			os.system('java -jar /home/tools/VarScan/VarScan.v2.3.3.jar mpileup2snp %s/%s.pileup > %s/%s.snp 2> %s/%s.snp.qlog &' % \
				(inputDirN,sampN, outputDirN,sampN, outputDirN,sampN))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

optH = mybasic.parseParam(optL)

main('/EQL1/NSL/Exome/mutation', '/EQL1/NSL/Exome/mutation', True)
