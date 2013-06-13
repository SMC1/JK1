#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def main(sId, inFileName, outFileName, minCover=4, minMutReads=2, minFreq=0.01):

	minCover = int(minCover)
	minFreq = float(minFreq)

	outFile = open(outFileName,'w')

	inFile = open(inFileName)
	
	for line in inFile:

		if line[0] == '#':
			continue

		tL = line[:-1].split('\t')

		qual = tL[5]
		
		if float(qual) < 15:
			continue

		if tL[3] == tL[4]:
			continue

		chr = tL[0]
		pos = tL[1]
		refAllele = tL[3]
		mutAllele = tL[4]

		format = tL[8]
		fL = format.split(':')
		idxAD = fL.index('AD')
		idxDP = fL.index('DP')

		sample = tL[9]
		sL = sample.split(':')
		
		refCount = int(sL[idxAD].split(',')[0])
		mutCount = int(sL[idxAD].split(',')[1])
		totCount = refCount + mutCount
		
#		if totCount != int(sL[idxDP]):
#			print line
		
		if totCount < minCover:
			#print 'skip cover:',tL[1],minCover
			continue

		freq = float(mutCount)/totCount

		if mutCount < int(minMutReads) or freq  < float(minFreq):
			#print 'skip freq:',freq,minFreq
			continue

		outFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%.3f\n' % (chr,pos,refAllele,mutAllele,refCount,mutCount,freq))
		
	outFile.close()


optL, argL = getopt.getopt(sys.argv[1:],'s:i:o:c:m:f:',[])

optH = mybasic.parseParam(optL)

sId = optH['-s']
inFileName = optH['-i']
outFileName = optH['-o']
minCover = optH['-c']
minMutReads = optH['-m']
minFreq = optH['-f']

main(sId,inFileName,outFileName,minCover,minMutReads,minFreq)
