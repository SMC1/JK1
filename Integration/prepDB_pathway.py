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
#	main(optH['-i'], optH['-o'])

#main('/EQL1/NSL/array_gene/NSL_GBM_93_zNorm.gct',['EGFR','TNC'],'S')
#main('/EQL1/NSL/array_gene/NSL_GBM_93_zNorm.gct',[],'S')
#main('/data1/CCLE_Sanger/CCLE_Expression_Entrez_2012-09-29_madNorm.gct')
main('/EQL1/TCGA/GBM/array_gene/TCGA_GBM_BI_pathway.gct',['TGFb'],'')
