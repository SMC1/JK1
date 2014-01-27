#!/usr/bin/python

import sys, getopt
import mybasic

def main(inFileName, ToutFileName):

	inFile = open(inFileName)
	ToutFile = open(ToutFileName,'w')

	inFile.readline()
	
	for line in inFile:

		dataL = line[:-1].split('\t')

		chr = dataL[0]
		start = dataL[1]
		ref = dataL[2]
		obs = dataL[3]

		nr1 = int(dataL[4])
		nr2 = int(dataL[5])
		tr1 = int(dataL[8])
		tr2 = int(dataL[9])
		
		type = dataL[12]

		if type != 'LOH':
			continue

		# normal - hetero.
		minF = min(float(nr1)/float(nr1+nr2), float(nr2)/float(nr1+nr2))

		if minF < 0.4:
			continue

#		if nr1+nr2 < 10:
#			continue
		
		maxF = max(float(tr1)/float(tr1+tr2), float(tr2)/float(tr1+tr2))

		ToutFile.write('%s\t%s\t%s\t%s\t%d\t%d\t%.4f\n' %(chr,start,ref,obs,tr1,tr2,maxF))

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:
	main(optH['-i'],optH['-o'])

