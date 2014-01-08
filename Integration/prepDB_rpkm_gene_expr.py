#!/usr/bin/python

import sys, getopt
import mybasic


def main(inGctFileName,geneList=[],samplePrefix=''):

	inFile = open(inGctFileName)

	inFile.readline()
	inFile.readline()

	sampleIdL = inFile.readline()[:-1].split('\t')

	for line in inFile:

		dataL = line[:-1].split('\t')

		if geneList==[] or dataL[0] in geneList:
			
			for i in range(2,len(dataL)):
				sys.stdout.write('%s%s\t%s\t%.4f\n' % (samplePrefix,sampleIdL[i],dataL[0],float(dataL[i])))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:t',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#
#	main(optH['-i'], optH['-o'])

#main('/EQL1/NSL/RNASeq/expression/NSL_RPKM_36.gct',[],'S')
#main('/EQL1/NSL/RNASeq/results/expression/NSL_RPKM_45.gct',[])
#main('/EQL1/NSL/RNASeq/expression/NSL_RPKM_41.gct',[])
#main('/EQL2/SGI_20131031/RNASeq/results/expression/RPKM_30.gct',[])
#main('/EQL1/NSL/RNASeq/results/expression/SGI20131119_6.gct',[])
main('/EQL1/NSL/RNASeq/results/expression/SGI20131212_6.gct',[])
