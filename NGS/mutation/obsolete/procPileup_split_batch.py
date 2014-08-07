#!/usr/bin/python

import sys, os, re, getopt, glob
import mybasic


def main(inDirName,outDirName,pbs=False):

	fileNameL = glob.glob('%s/*.pileup' % inDirName)

	print 'Files: %s (%s)' % (fileNameL, len(fileNameL))

	sampNameL = list(set([re.search('\/([^/]*)\.pileup',inputFileN).group(1) for inputFileN in fileNameL]))
	sampNameL.sort()

	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

		print sampN

		cmd = '~/JK1/NGS/mutation/procPileup_split.py -i %s/%s.pileup -o %s -q 15; gzip %s/%s.pileup' % (inDirName,sampN, outDirName, inDirName,sampN)
		log = '%s/%s.pileup_proc.log' % (outDirName,sampN)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))
		else:
			os.system('(%s) 2> %s' % (cmd, log))


#optL, argL = getopt.getopt(sys.argv[1:],'i:e:o:l:',[])
#
#optH = mybasic.parseParam(optL)
#
#if '-i' in optH and '-o' in optH:
#
#	main(optH['-i'], '', optH['-o'], '-t' in optH)

if __name__ == '__main__':
	main('/pipeline/ExomeSeq_20130723/S437_T_SS', '/pipeline/ExomeSeq_20130723/S437_T_SS', False)
