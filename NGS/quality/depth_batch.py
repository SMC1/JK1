#!/usr/bin/python

import sys, os, re, getopt, glob
import mybasic


def main(inDirName,outDirName):

	fileNameL = glob.glob('%s/*.pileup' % inDirName)

	print 'Files: %s (%s)' % (fileNameL, len(fileNameL))

	sampNameL = list(set([re.match('.*\/([^/]*)\.pileup',inputFileN).group(1) for inputFileN in fileNameL]))
	sampNameL.sort()

	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

		if '671T' in sampN:
			continue

		print sampN

		os.system('echo "~/JK1/NGS/quality/depth.py -i %s/%s.pileup -o %s/%s.depth" | qsub -N %s -o %s/%s.depth.qlog -j oe' \
			% (inDirName,sampN, outDirName,sampN, sampN, outDirName,sampN))


if __name__ == '__main__':

	#optL, argL = getopt.getopt(sys.argv[1:],'i:e:o:l:',[])
	#optH = mybasic.parseParam(optL)
	
	main('/EQL1/NSL/Exome/mutation','/EQL1/NSL/Exome/mutation')
