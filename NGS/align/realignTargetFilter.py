#!/usr/bin/python

import sys, getopt, re
import mybasic, mygenome


def loadExonH():

	exnH = {}

	kgH = mygenome.loadKgByChr()

	for chrom in kgH.keys():
		
		if chrom not in exnH:
			exnH[chrom] = []

		for tH in kgH[chrom]:

			for i in range(len(tH['exnList'])):
				exnH[chrom].append(tH['exnList'][i])

		exnH[chrom] = list(set(exnH[chrom]))

		exnH[chrom].sort(lambda x,y: cmp(x[0],y[0]))
		exnH[chrom].sort(lambda x,y: cmp(x[1],y[1]))

#	refFlatH = mygenome.loadRefFlatByChr()
#
#	for chrom in refFlatH.keys():
#		
#		if chrom not in exnH:
#			exnH[chrom] = []
#
#		for tH in refFlatH[chrom]:
#
#			for i in range(len(tH['exnList'])):
#				exnH[chrom].append(tH['exnList'][i])
#
#		exnH[chrom] = list(set(exnH[chrom]))
#
#		exnH[chrom].sort(lambda x,y: cmp(x[0],y[0]))
#		exnH[chrom].sort(lambda x,y: cmp(x[1],y[1]))

	return exnH


def main():

	exnH = loadExonH()

	exnChr = 'chr1'
	exnIdx = 0

	for line in sys.stdin:

		chrom = line.split(':')[0]
		tail = line[:-1].split(':')[1].split('-')

		if chrom==exnChr and exnIdx == len(exnH[exnChr]):
			continue

		if len(tail) == 1:
			chrSta = chrEnd = int(tail[0])
		else:
			chrSta = int(tail[0])
			chrEnd = int(tail[1])

		if chrom != exnChr:
			exnChr = chrom
			exnIdx = 0

		while exnH[exnChr][exnIdx][1] < chrEnd:
			exnIdx += 1
			if exnIdx == len(exnH[exnChr]):
				break

		if exnIdx < len(exnH[exnChr]) and exnH[exnChr][exnIdx][0] < chrSta and chrEnd <= exnH[exnChr][exnIdx][1]:
			sys.stdout.write(line)


#optL, argL = getopt.getopt(sys.argv[1:],'i:o:s:',[])
#optH = mybasic.parseParam(optL)

main()
