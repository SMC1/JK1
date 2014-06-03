#!/usr/bin/python

import sys, os, re, getopt, MySQLdb
import mybasic

def main(inDirName, inFilePattern, outDirName):
	fileNameL = os.listdir(inDirName)
	fileNameL = filter(lambda x: re.match(inFilePattern, x), fileNameL)

	print 'Files: %s (%s)' % (fileNameL, len(fileNameL))

	sampNameL = list(set([re.match(inFilePattern, inputFile).group(1) for inputFile in fileNameL]))
	sampNameL.sort()

	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	mutscanFL = filter(lambda x: re.match('(.*)\.mutscan$', x), os.listdir(inDirName))

	for sampN in sampNameL:
		os.system('(python ~/JK1/NGS/mutation/annotate_join_cosmic.py -i %s -s %s -o %s) &> %s/%s.cosmic.log' % (inDirName, sampN, outDirName, outDirName, sampN))

if __name__ == '__main__':
	main('/pipeline/test_ini_rsq2mut2/S096_RSq', '(.*)\.vep$', '/pipeline/test_ini_rsq2mut2/S096_RSq')
