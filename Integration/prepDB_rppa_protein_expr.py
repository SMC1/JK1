#!/usr/bin/python

import sys, getopt
import mybasic


def main(inGctFileName,samplePrefix=''):

	inFile = open(inGctFileName)

	inFile.readline()
	inFile.readline()

	sampleIdL = inFile.readline()[:-1].split('\t')

	for line in inFile:

		dataL = line[:-1].split('\t')

		geneNL = dataL[1].split(' ')

		for i in range(2,len(dataL)):
			sys.stdout.write('%s%s\t%s\t%s\t%.4f\n' % (samplePrefix,sampleIdL[i],dataL[0],','.join(geneNL),float(dataL[i])))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:t',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#
#	main(optH['-i'], optH['-o'])

main('/EQL1/TCGA/GBM/RPPA/TCGA_GBM_RPPA.gct',[])
