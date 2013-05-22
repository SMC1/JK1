#!/usr/bin/python

import sys, getopt
import mybasic

def main(inFileName, sampN, outFileName):

	inFile = open(inFileName)
	outFile = open(outFileName,'w')

	inFile.readline()
	
	count = 0

	for line in inFile:

		dataL = line[:-1].split('\t')

		chr = dataL[0]
		start = int(dataL[1])-1
		end = dataL[1]
		ref = dataL[2]
		obs = dataL[3]
		somatic = dataL[12]

		if obs=='N' or ref=='N':
			continue

		if somatic != 'Somatic':
			continue

		count += 1
		
		obsL = obs.split('/')
		
		for i in range(len(obsL)):
			outFile.write('%s\t%s\t%s\t%s\t+\t%s\t%s\t%s\n' % (count,chr,start,end,ref,obsL[i],sampN))

optL, argL = getopt.getopt(sys.argv[1:],'i:s:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:
	main(optH['-i'],optH['-s'],optH['-o'])
