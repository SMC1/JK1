#!/usr/bin/python

import sys, getopt
import mybasic

def main(inFileName, outFileName):

	inFile = open(inFileName)
	outFile = open(outFileName,'w')

	inFile.readline()

	for line in inFile:

		dataL = line[:-1].split('\t')

		chr = dataL[0]
		start = dataL[1]
		end = dataL[1]
		ref = dataL[2]
		obs = dataL[3]

		outFile.write('%s\t%s\t%s\t%s\t%s\n' % (chr,start,end,ref,obs))

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:
	main(optH['-i'],optH['-o'])
