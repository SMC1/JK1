#!/usr/bin/python

import sys, getopt, math
import mybasic, mygenome

def main(inFileName, outFileName, inRefFlatFileName='/data1/Sequence/ucsc_hg19/annot/refFlat.txt', assembly='hg19'):

	geneNameL = list(set([line.split('\t')[0] for line in open(inRefFlatFileName)]))
	geneNameL.sort()

	inFileL = [line[:-1].split('\t') for line in open(inFileName) if line[:-1].split('\t')[0] != 'ID']

	outFile = open(outFileName, 'w')

	for geneName in geneNameL:

		try:
			trans = mygenome.transcript(geneName,inRefFlatFileName,assembly)
		except:
			continue

		for dataL in inFileL:

			(sId, chrNum, chrSta, chrEnd, type, cn) = dataL

			overlap = trans.cdsOverlap((chrNum,int(chrSta),int(chrEnd)))
			
			if overlap > 0:

				if type != 'gain':
					outFile.write('%s\t%s\t%s\n' % (sId,geneName,type))
	
optL, argL = getopt.getopt(sys.argv[1:],'i:o:r:a:',[])

optH = mybasic.parseParam(optL)

if  '-i' in optH and '-o' in optH:
	main(optH['-i'],optH['-o'])
