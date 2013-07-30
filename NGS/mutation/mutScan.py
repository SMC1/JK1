#!/usr/bin/python

import sys, os, re, getopt
import mybasic


chromL = map(lambda x: 'chr'+x, map(str,range(1,23))+['X','Y','M'])

def main(sId, inDirName, outFileName, minCover=4, minMutReads=2, minFreq=0.01):

	minCover = int(minCover)
	minFreq = float(minFreq)

	outFile = open(outFileName,'w')

	for chrom in chromL:

		if '%s_%s.pileup_proc' % (sId,chrom) in os.listdir(inDirName) :
			inFile = open('%s/%s_%s.pileup_proc' % (inDirName,sId,chrom)) 
		else : 
			continue

		for line in inFile:

			tL = line[:-1].split(',')

			if tL[1] == tL[3]:
				continue

			if int(tL[1]) < minCover:
				#print 'skip cover:',tL[1],minCover
				continue

			chrPos = tL[0]
			totCount = int(tL[1])
			refAllele = tL[2]
			refCount = int(tL[3])
			mutBaseStr = tL[4]

			for mutAllele in ['A','T','G','C']:

				mutCount = mutBaseStr.count(mutAllele)
				freq = float(mutCount)/totCount

				if mutCount < int(minMutReads) or freq  < float(minFreq):
					#print 'skip freq:',freq,minFreq
					continue

				outFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%.3f\n' % (tuple(chrPos.split(':'))+(refAllele,mutAllele,refCount,mutCount,freq)))
				
	outFile.close()
	
	print 'Success: %s' % inFileTitle

optL, argL = getopt.getopt(sys.argv[1:],'s:i:o:c:m:f:',[])

optH = mybasic.parseParam(optL)

sId = optH['-s']
inDirName = optH['-i']
outFileName = optH['-o']
minCover = optH['-c']
minMutReads = optH['-m']
minFreq = optH['-f']

main(sId,inDirName,outFileName,minCover,minMutReads,minFreq)
