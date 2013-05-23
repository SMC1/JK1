#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def main(inDirName,outDirName,fileNamePattern,pbs):

	fileNameL = os.listdir(inDirName)
	fileNameL = filter(lambda x: re.match(fileNamePattern, x), fileNameL)

	print 'Files: %s (%s)' % (fileNameL, len(fileNameL))

	sampNameL = list(set([re.match(fileNamePattern,inputFileN).group(1) for inputFileN in fileNameL]))
	sampNameL.sort()

	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL[1:]:

		print sampN

		if pbs:
			os.system('echo "~/JK1/NGS/mutation/procPileup_split.py -i %s/%s.pileup -o %s -q 15" | qsub -N %s -o %s/%s.pileup_proc.log -j oe' % \
				(inDirName,sampN, outDirName, sampN, outDirName,sampN))
		else:
			os.system('(~/JK1/NGS/mutation/procPileup_split.py -i %s/%s.pileup -o %s -q 15) 2> %s/%s.pileup_proc.log' % (inDirName,sampN, outDirName, outDirName,sampN))


#optL, argL = getopt.getopt(sys.argv[1:],'i:e:o:l:',[])
#
#optH = mybasic.parseParam(optL)
#
#if '-i' in optH and '-o' in optH:
#
#	main(optH['-i'], '', optH['-o'], '-t' in optH)

main('/EQL1/NSL/exome_bam/mutation/link', '/EQL1/NSL/exome_bam/mutation/link/proc', '(.*)\.pileup', True)
