#!/usr/bin/python

import sys, getopt, re
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
#				sampId = re.match('X([0-9]{3}).*',sampleIdL[i]).group(1)
				sampId = re.match('(.*)', sampleIdL[i]).group(1)
				sys.stdout.write('%s%s\t%s\t%.4f\n' % (samplePrefix,sampId,dataL[0],float(dataL[i])))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:t',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#
#	main(optH['-i'], optH['-o'])

#main('/EQL1/NSL/array_gene/NSL_GBM_93_zNorm.gct',['EGFR','TNC'],'S')
#main('/EQL1/NSL/CGH/NSL_GBM_cn_109.gct',[],'S')
#main('/EQL1/TCGA/GBM/array_gene/TCGA_GBM_gene_BI_sIdClps_zNorm.gct')

#main('/EQL1/TCGA/GBM/array_cn/TCGA_GBM_CNA_SNP6_tumorOnly.gct')

#main('/data1/IRCR/CGH/seg/copyNumber_NSL102_sIdClps.gct',[],'S')

#main('/data1/CCLE_Sanger/CCLE_copynumber_2012-09-29.gct',[],'')
main('/EQL1/NSL/CGH/CGH_352_363.gct', [], '')
