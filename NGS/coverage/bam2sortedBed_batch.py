#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def sam2bed_batch(inputDirN,outputDirN,pbs=False):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('.*\.bam', x),inputFileNL)
	sampNameS = set([re.match('(.*)\.bam',inputFileN).group(1) for inputFileN in inputFileNL])

#	excSampNameS = set([re.match('.*/(.*).qlog:100\.0.*',line).group(1) for line in os.popen('grep -H 100.0 %s/*.qlog' % outputDirN)])
#	sampNameS = sampNameS.difference(excSampNameS)

	sampNameL = list(sampNameS)
	sampNameL.sort()

	print 'Samples: %s (%s)' % (sampNameL,len(sampNameL))

	for sampN in sampNameL:

#		if sampN[7:-5] not in ['TCGA-28-5216-01A-01R-1850-01.4']:
#			continue

		if pbs:

			os.system('echo "bamToBed -i %s/%s.bam | sort -k1,1 -k2,2n > %s/%s.sorted.bed" | \
				qsub -N %s -o %s/%s.bed.qlog -j oe' % (inputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))

		else:

			print sampN

			os.system('(bamToBed -i %s/%s.bam | sort -k1,1 -k2,2n > %s/%s.sorted.bed) 2> %s/%s.sorted.bed.qlog' % \
				(inputDirN,sampN, outputDirN,sampN, outputDirN,sampN))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

optH = mybasic.parseParam(optL)

inputDirN = optH['-i']

if '-o' in optH:
	outputDirN = optH['-o']
else:
	outputDirN = inputDirN

sam2bed_batch(inputDirN,outputDirN,'-p' in optH)
