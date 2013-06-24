#!/usr/bin/python

import sys, getopt
import mybasic, mygsnap


def filter_transloc(inFileName,outFileName):

	result = mygsnap.gsnapFile(inFileName,False)
	outFile = open(outFileName, 'w')

	count_all = 0
	count_transloc = 0

	for r in result:

		count_all += 1

		if not '(transloc)' in r.pairRel:
			continue

		match = r.matchL()[0]

		segObjL = match.getSegInfo()

		skip = False

		for segObj in segObjL:
			if segObj.span - segObj.numMatch > 2 or segObj.percMatch < 90 or segObj.span < 5:
				skip = True
				break

		if skip:
			continue

		outFile.write(r.rawText()+'\n')
		count_transloc += 1

	print 'Results:',count_transloc,count_all

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:

	filter_transloc(optH['-i'], optH['-o'])
