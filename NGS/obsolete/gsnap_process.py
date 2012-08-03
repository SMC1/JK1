#!/usr/bin/python

import sys
import mygsnap, mygenome



if len(sys.argv) >= 3:
	inFileName = sys.argv[1]
	outFileName = sys.argv[2]
else: # this is default file, analysis specific files should be indicated as commandline arguments
	inFileName = 'GH_ft.txt'
	outFileName = 'GH_ft_process.txt'


refFlatFileName = '/home/gye_hyeon/RNASeq/code_jk/refFlat_hg19.txt'
resolveGene = False


result = mygsnap.gsnapFile(inFileName)
outFile = open(outFileName, 'w')

if resolveGene:
	refFlatH = mygenome.loadRefFlatByChr(refFlatFileName)

for rL in result:

	for i in (0,1):

		outFile.write(','.join([x.toString() for x in rL[i].matchL()[0].mergedLocusL()]) + '\t')

		if resolveGene:

			overlappingGeneL = []

			for loc in rL[i].locusMergedL:
				overlappingGeneL += loc.overlappingGeneL(refFlatH=refFlatH)

			outFile.write(','.join(overlappingGeneL))

		if i == 0:
			outFile.write('\t')

	outFile.write('\n')
