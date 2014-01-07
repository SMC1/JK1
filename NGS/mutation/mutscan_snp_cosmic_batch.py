#!/usr/bin/python

import sys, os, re, getopt
import mybasic
from glob import glob


def main(inDirName):

	inputFileNL = os.listdir(inDirName)
	inputFileNL = filter(lambda x: re.match('(.*)\.mutscan$', x),inputFileNL)

	print 'Files: %s' % inputFileNL, len(inputFileNL)

	sampNL = list(set([re.match('(.*)\.mutscan',inputFileN).group(1) for inputFileN in inputFileNL]))
	sampNL.sort()

	print 'samples: %s' % sampNL

	for sampN in sampNL:

#		if sampN not in ['S022_T_KN']:
#			continue
		if '_B_' in sampN or '_N_' in sampN:
			continue

		print sampN

		if glob('%s/%s_cosmic.dat' % (inDirName,sampN)):
			os.system('(rm %s/%s_cosmic.dat;\
			python ~/JK1/NGS/mutation/mutscan_snp_cosmic.py -d %s -i %s.mutscan -o %s_cosmic.dat -s %s) &> %s/%s.cosmic.log' % \
			(inDirName,sampN, inDirName, sampN, sampN, sampN, inDirName,sampN))
		else:
			os.system('(python ~/JK1/NGS/mutation/mutscan_snp_cosmic.py -d %s -i %s.mutscan -o %s_cosmic.dat -s %s) &> %s/%s.cosmic.log' % \
			(inDirName, sampN, sampN, sampN, inDirName,sampN))

if __name__ == '__main__':

# to batch processing samples
#	projDir = '/EQL1/pipeline/SGI20131119_rsq2mut'
#	projDir = '/EQL3/pipeline/SGI20131216_xsq2mut'
#	inputDirNL = os.listdir(projDir)
#	inputDirL = filter(lambda x: os.path.isdir('%s/%s' % (projDir,x)), inputDirNL)
#
#	for inputDir in inputDirL:
#		main('%s/%s' % (projDir, inputDir))
# to process every individual samples
#	optL, argL = getopt.getopt(sys.argv[1:],'i:',[])
#
#	optH = mybasic.parseParam(optL)
#
#	main('/pipeline/ExomeSeq_20130723/S437_T_SS')
