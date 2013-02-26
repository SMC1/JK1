#!/usr/bin/python

import sys, getopt, re
import mybasic


def main(inFileName):

	inFile = open(inFileName)

	for line in inFile:

		dataL = line[:-1].split('\t')

		(sampN,loc1,loc2,exon1,exon2,nReads,nPos) = (dataL[0],dataL[1],dataL[2],dataL[3],dataL[4],dataL[5],dataL[7])

		sampN = re.search('[^L]?([0-9]{3})',sampN).group(1)

		sys.stdout.write('S%s\t%s\t%s\t%s\t%s\n' % (sampN,loc1,loc2,nReads,nPos))
		#sys.stdout.write('S%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (sampN,loc1,loc2,exon1,exon2,nReads,nPos))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#	main(optH['-i'], optH['-o'])

main('/EQL1/NSL/RNASeq/alignment/splice_normal_NSL36.txt')
