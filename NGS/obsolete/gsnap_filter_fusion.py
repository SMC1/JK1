#!/usr/bin/python

import sys
import mygsnap



if len(sys.argv) >= 3:
	inFileName = sys.argv[1]
	outFileName = sys.argv[2]
else:
	inFileName = '/Data2/RNASeq_SMC1_S02_result.txt'
	outFileName = 'GH_S02_matchfilter2.txt'

matchCutOff = 90

result = mygsnap.gsnapFile(inFileName)
outFile = open(outFileName, 'w')


for rL in result:

	if not (rL[0].nLoci==1 and rL[1].nLoci==1 and rL[0].pairRel=='unpaired') or '(transloc)' in rL[0].pairRel:
		continue

	if not (len(rL[0].matchL()[0].mergedLocusL())==1 and len(rL[1].matchL()[0].mergedLocusL())==1):
		continue

	if not (rL[0].matchL()[0].numMatch()>=matchCutOff and rL[1].matchL()[0].numMatch()>=matchCutOff):
		continue

	for i in (0,1):
		outFile.write(rL[i].rawText()+'\n')
