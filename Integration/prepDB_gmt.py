#!/usr/bin/python

import sys, getopt, re
import mybasic

def main(inFileName):

	inFile = open(inFileName)

	for line in inFile:

		valueL = line[:-2].split('\t') # line[:-1].split('\t')

		id = valueL[0]
		desc = valueL[1]
		geneL = valueL[2:]
		
		for i in range(len(geneL)):

			sys.stdout.write('%s\t%s\t%s\n' % (id, desc, geneL[i]))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#	main(optH['-i'], optH['-o'])

main('/data1/Sequence/geneinfo/KEGG.gmt')
