#!/usr/bin/python

import sys, getopt
import mybasic, mygsnap


def filter_crossMap(inFileName,outFileName):

	result = mygsnap.gsnapFile(inFileName,True)
	outFile = open(outFileName, 'w')

	count_all = 0
	count_crossMap = 0

	for rL in result:

		if rL[0].nLoci==1 and rL[1].nLoci==1 and rL[0].pairRel=='unpaired':

			for i in (0,1):
				outFile.write(rL[i].rawText()+'\n')

			count_crossMap += 1

		count_all += 1

	print count_crossMap,count_all


optL, argL = getopt.getopt(sys.argv[1:],'i:o:t',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:

	filter_crossMap(optH['-i'], optH['-o'])
