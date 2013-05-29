#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def main(inDirName):

	inputFileNL = os.listdir(inDirName)
	inputFileNL = filter(lambda x: re.match('(.*)\.mutscan', x),inputFileNL)

	print 'Files: %s' % inputFileNL, len(inputFileNL)

	sampNL = list(set([re.match('(.*)\.mutscan',inputFileN).group(1) for inputFileN in inputFileNL]))
	sampNL.sort()

	print 'samples: %s' % sampNL

	for sampN in sampNL:

#		if sampN not in ['S022_T_KN']:
#			continue

		print sampN

		os.system('python mutscan_snp_cosmic.py -d %s -i %s.mutscan -o %s_cosmic.dat -s %s' % \
			(inDirName, sampN, sampN, sampN))

optL, argL = getopt.getopt(sys.argv[1:],'i:',[])

optH = mybasic.parseParam(optL)

main('/EQL1/NSL/exome_bam/mutation/mutscan')
