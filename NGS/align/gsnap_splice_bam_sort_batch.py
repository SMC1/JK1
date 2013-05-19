#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def main(inputDirN, outputDirN, memSize):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('.*\.bam', x),inputFileNL)
	inputFileNL = filter(lambda x: not re.match('.*_sort.*', x),inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.bam',inputFileN).group(1) for inputFileN in inputFileNL]))

	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

	#	if not sampN in ['G17678.TCGA-06-5417-01A-01R-1849-01.2']:
	#		continue

		if '-p' in optH:

			print('%s' % sampN)
			os.system('echo "samtools sort -m %s %s/%s %s/%s.sorted" | qsub -N %s -o %s/%s.sort.qlog -j oe' % (memSize, inputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))

		else:

			print('%s' % sampN)
			os.system('(samtools sort -m %s %s/%s %s/%s.sorted) 2> %s/%s.sort.qlog' % (memSize, inputDirN,sampN, outputDirN,sampN, outputDirN,sampN))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

optH = mybasic.parseParam(optL)

#inputDirN = optH['-i']
#outputDirN = optH['-o']
#main(inputDirN, outputDirN)

main('/EQL1/NSL/RNASeq/alignment/splice/gatk_test', '/EQL1/NSL/RNASeq/alignment/splice/gatk_test',40000000000)
