#!/usr/bin/python

import sys, getopt, re
import mybasic, mygsnap


def bp_filter(inFileName,outFileName,expSize):
	'''
	filters gsnap records with (no-mismatch, no-indel, no-splicing) and (insert_length > N-nt)
	''' 

	result = mygsnap.gsnapFile(inFileName,True)
	outFile = open(outFileName, 'w')

	count_all = 0
	count_include = 0

	for rL in result:

		count_all += 1

		if rL[0].nLoci != 1 or rL[1].nLoci != 1:
			continue

		skip = False
		
		for i in (0,1):

			match = rL[i].matchL()[0]
			seg = match.getSegInfo()[0]

			if len(match.segL) > 1 or match.pairInfo()[0] < 1000 or match.pairInfo()[0] > 10000 or (seg.len - seg.numMatch) > 0:
				skip = True
				break

		if skip:
			continue

		for i in (0,1):
			print rL[i].rawText()
			print rL[i].matchL()[0].getSegInfo()[0].len, rL[i].matchL()[0].getSegInfo()[0].numMatch
			outFile.write(rL[i].rawText()+'\n')

		count_include += 1

	print count_include, count_all

optL, argL = getopt.getopt(sys.argv[1:],'i:o:l:',[])

optH = mybasic.parseParam(optL)

bp_filter(optH['-i'], optH['-o'], int(optH['-l']))
