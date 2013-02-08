#!/usr/bin/python

import sys, getopt, re
import mybasic


def main(inGctFileName,geneList=None):

	inFile = open(inGctFileName)

	headerL = inFile.readline()[:-1].split('\t')

	for line in inFile:

		dataL = line[:-1].split('\t')

		if geneList and dataL[5] in geneList:

			(sampN,loc1,loc2,geneN,exon1,exon2,frame,nPos) = (dataL[0],dataL[1],dataL[2],dataL[5],dataL[3],dataL[4],dataL[6],dataL[-1])

			sampN = re.search('[^L]?([0-9]{3})',sampN).group(1)

			sys.stdout.write('S%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (sampN,loc1,loc2,geneN,exon1,exon2,frame,nPos))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#	main(optH['-i'], optH['-o'])

main('/EQL1/NSL/RNASeq/alignment/splice_skipping_NSL36.txt',['EGFR'])
