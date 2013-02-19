#!/usr/bin/python

import sys, getopt
import mybasic


def main(inGctFileName,geneList=None):

	inFile = open(inGctFileName)

	inFile.readline()
	inFile.readline()

	sampleIdL = inFile.readline()[:-1].split('\t')

	for line in inFile:

		dataL = line[:-1].split('\t')

		if geneList and dataL[0] in geneList:
			
			for i in range(2,len(dataL)):
				sys.stdout.write('S%s\t%s\t%s\n' % (sampleIdL[i],dataL[0],dataL[i]))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:t',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#
#	main(optH['-i'], optH['-o'])

main('/EQL1/NSL/array_gene/NSL_GBM_93_zNorm.gct',['EGFR','TNC'])
