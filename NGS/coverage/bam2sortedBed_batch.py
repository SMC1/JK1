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
		print sampN

		iprefix = '%s/%s' % (inputDirN,sampN)
		oprefix = '%s/%s' % (outputDirN,sampN)
		cmd = 'bamToBed -i %s.bam | sort -k1,1 -k2,2n > %s.sorted.bed' % (iprefix, oprefix)
		log = '%s.sorted.bed.qlog' % (oprefix)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))

		else:
			os.system('(%s) 2> %s' % (cmd, log))



if __name__ == '__main__':
#	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])
#
#	optH = mybasic.parseParam(optL)
#
#	inputDirN = optH['-i']
#
#	if '-o' in optH:
#		outputDirN = optH['-o']
#	else:
#		outputDirN = inputDirN
#
	sam2bed_batch('/EQL2/TCGA/LUAD/RNASeq/alignment/30nt','/EQL2/TCGA/LUAD/RNASeq/coverage',pbs=True)
	#sam2bed_batch(inputDirN,outputDirN,'-p' in optH)
