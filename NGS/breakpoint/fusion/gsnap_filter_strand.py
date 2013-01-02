#!/usr/bin/python

import sys, getopt
import mybasic, mygsnap


def filter_strand(inFileName,outFileName):

	result = mygsnap.gsnapFile(inFileName,True)
	outFile = open(outFileName, 'w')

	count_all = 0
	count_strand = 0

	for rL in result:

		if not (rL[0].nLoci==1 and rL[1].nLoci==1 and rL[0].pairRel=='unpaired'):
			raise Exception

		chrom0 = rL[0].matchL()[0].segL[0][2].split(':')[0]
		chrom1 = rL[1].matchL()[0].segL[0][2].split(':')[0]

		if ((chrom0[0]==chrom0[-1] and chrom1[0]!=chrom1[-1]) or (chrom0[0]!=chrom0[-1] and chrom1[0]==chrom1[-1])) and chrom0[1:-1]!=chrom1[1:-1]:

			for i in (0,1):
				outFile.write(rL[i].rawText()+'\n')

			count_strand += 1

		else:

			for i in (0,1):
				print rL[i].rawText()

		count_all += 1

	print count_strand, count_all


optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:

	filter_strand(optH['-i'], optH['-o'])
