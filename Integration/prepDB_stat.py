#!/usr/bin/python

import sys, getopt, numpy
import mybasic


def main(inGctFileName,geneList=[]):

	inFile = open(inGctFileName)

	inFile.readline()
	inFile.readline()

	sampleIdL = inFile.readline()[:-1].split('\t')

	for line in inFile:

		dataL = line[:-1].split('\t')
		valueL = map(float,dataL[2:])
		valueL = sorted(valueL)

		b = int((25)*0.01*len(valueL))
		t = int((75)*0.01*len(valueL))

#		iqr = float(valueL[t]) - float(valueL[b])

		sys.stdout.write('%s\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\n' % (dataL[0],valueL[b], numpy.median(valueL),valueL[t],numpy.mean(valueL),numpy.std(valueL)))
#		out1 = float(valueL[t]) + (iqr * 3)
#		out2 = float(valueL[b]) - (iqr * 3)
		
#		if geneList==[] or dataL[0] in geneList:
#			
#			for i in range(2,len(dataL)):
#
#				if float(dataL[i]) >= out1 or float(dataL[i]) <= out2:
#					sys.stdout.write('%s%s\t%s\t%.4f\n' % (samplePrefix,sampleIdL[i],dataL[0],float(dataL[i])))

optL, argL = getopt.getopt(sys.argv[1:],'i:o',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#
#	main(optH['-i'], optH['-o'])

#main('/EQL1/NSL/array_gene/NSL_GBM_93_zNorm.gct',['EGFR','TNC'],'S')
main('/data1/CCLE_Sanger/CCLE_Expression_Entrez_2012-09-29_madNorm.gct')
#main('/EQL1/NSL/array_gene/NSL_GBM_93_madNorm.gct')
#main('/EQL1/TCGA/GBM/array_gene/TCGA_GBM_gene_BI_sIdClps_madNorm.gct')
