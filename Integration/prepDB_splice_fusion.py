#!/usr/bin/python

import sys, getopt, re
import mybasic


def main(inGctFileName,minNPos,sampNamePat=('(.*)',''),geneList=[]):

	inFile = open(inGctFileName)

	headerL = inFile.readline()[:-1].split('\t')

	for line in inFile:

		d = line[:-1].split('\t')

		if not geneList or set(d[7].split(';')+d[8].split(';')).intersection(geneList):

			(sampN,loc1,loc2,geneN1,geneN2,ftype,exon1,exon2,frame,nReads,nPos) = (d[0],d[3],d[4],d[7],d[8],d[1],d[5],d[6],d[9],d[-3],d[-1])

			if int(nPos) < minNPos:
				continue

			sampN = re.search(sampNamePat[0],sampN).group(1)
			
			geneN1 = ','.join(set(geneN1.split(';'))-set(['']))
			geneN2 = ','.join(set(geneN2.split(';'))-set(['']))

			sys.stdout.write('%s%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (sampNamePat[1],sampN,loc1,loc2,geneN1,geneN2,ftype,exon1,exon2,frame,nReads,nPos))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#	main(optH['-i'], optH['-o'])

#main('/EQL1/NSL/RNASeq/alignment/splice_fusion_NSL36.txt',1,('[^L]?([0-9]{3})','S'))
#main('/EQL3/TCGA/GBM/RNASeq/alignment/splice_fusion_170.txt',1,('.*(TCGA-..-....).*',''))
main('/EQL1/NSL/RNASeq/results/fusion/splice_fusion_NSL43.txt',1,('([0-9]{3})','S'))
