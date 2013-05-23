#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def main(inputDirN, outputDirN):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = set(filter(lambda x: re.match('(.*)\.snp', x),inputFileNL))
	exNL = set(filter(lambda x: re.match('(.*)\.snp.\qlog', x),inputFileNL))
	inputFileNL = list(inputFileNL - exNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.snp',inputFileN).group(1) for inputFileN in inputFileNL]))

	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

		if sampN not in ['NS08_567T_WXS','NS09_732T_WXS','NS07_464T_WXS','NS09_626T_WXS','GBM10_047T_WXS']:
			continue

		print sampN

		os.system('tail -q -n +2 %s/%s.snp > %s/%s_noheader.snp' % \
			(inputDirN,sampN, outputDirN,sampN))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

main('/EQL1/NSL/exome_bam/mutation', '/EQL1/NSL/exome_bam/mutation')
