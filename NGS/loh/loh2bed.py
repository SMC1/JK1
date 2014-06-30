#!/usr/bin/python

import sys, getopt, os
from glob import glob

def main(inFilePathL, outFileName):

	outFile = open(outFileName, 'w')

	for inFileName in inFilePathL:
		
		inFile = open(inFileName)
		inFile.readline()

		for line in inFile:

			(sId, chr, start, end, loh, cn) = line[:-1].split('\t')

			if loh != 'gain':
				outFile.write('chr%s\t%s\t%s\t%s\n' % (chr, start, end, sId))
	
main(glob('/EQL3/pipeline/Purity/*/*.loh_cn.txt'),'/EQL1/NSL/WXS/results/LOH/NSL_GBM_LOH_20140523.bed')
