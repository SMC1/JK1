#!/usr/bin/python

import sys, getopt, re
import mybasic


def main(inGctFileName,geneList=None):

	inFile = open(inGctFileName)

	headerL = inFile.readline()[:-1].split('\t')

	for line in inFile:

		d = line[:-1].split('\t')

		if geneList and set(d[7].split(';')+d[8].split(';')).intersection(geneList):

			(sampN,loc1,loc2,geneN1,geneN2,ftype,exon1,exon2,frame,nPos) = (d[0],d[3],d[4],d[7],d[8],d[1],d[5],d[6],d[9],d[-1])

			sampN = re.search('[^L]?([0-9]{3})',sampN).group(1)
			
			geneN1 = ','.join(set(geneN1.split(';'))-set(['']))
			geneN2 = ','.join(set(geneN2.split(';'))-set(['']))

			sys.stdout.write('S%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (sampN,loc1,loc2,geneN1,geneN2,ftype,exon1,exon2,frame,nPos))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#	main(optH['-i'], optH['-o'])

main('/EQL1/NSL/RNASeq/alignment/splice_fusion_NSL36.txt',['EGFR'])
