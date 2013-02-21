#!/usr/bin/python

import sys, getopt, re
import mybasic, mygsnap


def exonSkip_filter(inFileName,outFileName):
	'''
	filters-in exon-skipping candidates in splice-mapped gsnap
	''' 

	result = mygsnap.gsnapFile(inFileName, False)
	outFile = open(outFileName, 'w')

	count_all = 0
	count_include = 0

	for r in result:

		if r.nLoci != 1:
			continue
		
		match = r.matchL()[0]

		if len(match.segL) != 2:
			continue

		segObjL = match.getSegInfo()

		jncH = {}

		skip = False

		for segObj in segObjL:

			if segObj.span - segObj.numMatch > 2 or segObj.percMatch < 90 or segObj.span < 5:
				skip = True
				break

			if segObj.label == '':
				break

			for b in segObj.label.split('|'):

				rm2 = re.match('(.*)\.exon([0-9]+)\/[0-9]+',b)

				transId = rm2.group(1)
				exonNum = int(rm2.group(2))

				mybasic.addHash(jncH,transId,exonNum)

		if skip:
			continue

		jncL = jncH.items()
		
		if len(jncL)>0 and max([len(j[1]) for j in jncL])>1:

			minDist = 100

			for i in range(len(jncL)):

				if len(jncL[i][1]) == 2 and abs(jncL[i][1][0]-jncL[i][1][1]) < minDist:
					minDist = abs(jncL[i][1][0]-jncL[i][1][1])

			if minDist == 1: # only difference

				outFile.write(r.rawText()+'\n')
				count_include += 1

		count_all += 1

	print count_include, count_all

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:

	exonSkip_filter(optH['-i'], optH['-o'])
