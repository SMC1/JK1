#!/usr/bin/python

import sys, getopt, re
import mybasic, mygenome


def loadExonH():

	exnH = {}

	refFlatH = mygenome.loadRefFlatByChr()

	for chrom in refFlatH.keys():
		
		if chrom not in exnH:
			exnH[chrom] = []

		for tH in refFlatH[chrom]:

			for i in range(len(tH['exnList'])):
				exnH[chrom].append(tH['exnList'][i])

		exnH[chrom] = list(set(exnH[chrom]))

		exnH[chrom].sort(lambda x,y: cmp(x[1],y[1]))
		exnH[chrom].sort(lambda x,y: cmp(x[0],y[0]))

	return exnH


def main(inFilePath,outFilePath):

	exnH = loadExonH()

	depthH = {}

	exnChr = 'chr10'
	exnIdx = 0

	inFile = open(inFilePath)

	for line in inFile:

		tokL = line.split('\t')
		chrom, pos, cnt = tokL[0], int(tokL[1]), int(tokL[3])

		if chrom==exnChr and exnIdx==len(exnH[exnChr]):
			continue

		if chrom != exnChr:
			exnChr = chrom
			exnIdx = 0

		while exnIdx < len(exnH[exnChr]) and exnH[exnChr][exnIdx][1] < pos:
			exnIdx += 1

		if exnIdx < len(exnH[exnChr]) and exnH[exnChr][exnIdx][0] < pos <= exnH[exnChr][exnIdx][1]:
			mybasic.incHash(depthH,cnt,1)

	totalLen = 0

	for chrom in exnH:

		curPos = 0

		for exn in exnH[chrom]:

			curPos = max(curPos,exn[0])
			totalLen += exn[1]-curPos
			curPos = exn[1]
			
	depthH[0] = totalLen - sum(depthH.values())

	outFile = open(outFilePath,'w')

	for i in range(max(depthH.keys())+1):
		
		if i in depthH:
			d = depthH[i]
		else:
			d = 0

		outFile.write('%d\t%d\n' % (i,d))


if __name__ == '__main__':

	optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])
	optH = mybasic.parseParam(optL)

	main(optH['-i'],optH['-o'])
	#main('/EQL1/NSL/Exome/mutation/671T_Br1_WXS_trueSeq.pileup','/EQL1/NSL/Exome/mutation/671T_Br1_WXS_trueSeq.depth')
