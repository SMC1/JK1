#!/usr/bin/python

import sys, getopt
import mybasic, mygsnap


def filter_transloc(inFileName,outFileName):

	result = mygsnap.gsnapFile(inFileName,False)
	outFile = open(outFileName, 'w')

	count_all = 0
	count_transloc = 0

	for r in result:

		if '(transloc)' in r.pairRel:

			outFile.write(r.rawText()+'\n')
			count_transloc += 1

		count_all += 1

	print count_transloc,count_all

optL, argL = getopt.getopt(sys.argv[1:],'i:o:t',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:

	filter_transloc(optH['-i'], optH['-o'])
