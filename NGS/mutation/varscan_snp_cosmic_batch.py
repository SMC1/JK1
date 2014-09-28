#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def main(inDirName):

	inputFileNL = os.listdir(inDirName)
	inputFileNL = filter(lambda x: re.match('(.*)_noheader\.snp', x),inputFileNL)

	print 'Files: %s' % inputFileNL, len(inputFileNL)

	sampNL = list(set([re.match('(.*)_noheader\.snp',inputFileN).group(1) for inputFileN in inputFileNL]))
	sampNL.sort()

	print 'samples: %s' % sampNL

	for sampN in sampNL:

		if sampN not in ['NS08_567T_WXS','NS09_732T_WXS','NS07_464T_WXS','NS09_626T_WXS','GBM10_047T_WXS']:
			continue

		print sampN

		os.system('/usr/bin/python varscan_snp_cosmic.py -d %s -i %s_noheader.snp -o %s_snp_cosmic.dat -s %s' % \
			(inDirName, sampN, sampN, sampN))

optL, argL = getopt.getopt(sys.argv[1:],'i:',[])

optH = mybasic.parseParam(optL)

main('/EQL1/NSL/exome_bam/mutation')
