#!/usr/bin/python

import sys, getopt, re
import mybasic, mygsnap


def exonSkip_filter_annot(inFileName,outFileName):
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

		jncH = {}

		for i in range(len(match.segL)):

			rm1 = re.search('label_[12]:([^,\t]*)',match.segL[i][3])

			if not rm1:
				break

			for b in rm1.group(1).split('|'):

				rm2 = re.match('(.*)\.exon([0-9]+)\/[0-9]+',b)

				transId = rm2.group(1)
				exonNum = int(rm2.group(2))

				mybasic.addHash(jncH,transId,exonNum)

		jncL = jncH.items()
		
		if len(jncL)>0 and max([len(j[1]) for j in jncL])>1:

			minDist = 100

			for i in range(len(jncL)):

				if len(jncL[i][1]) == 2 and abs(jncL[i][1][0]-jncL[i][1][1]) < minDist:
					minDist = abs(jncL[i][1][0]-jncL[i][1][1])

			if minDist > 1:

				outFile.write(r.rawText()+'\n')
				count_include += 1

		count_all += 1

	print count_include, count_all

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:

	exonSkip_filter_annot(optH['-i'], optH['-o'])
