#!/usr/bin/python

import sys, getopt, re
import mybasic, mygsnap, mygenome


def loadExonH():

	exonH = {}

	refFlatH = mygenome.loadRefFlatByChr()

	for chrom in refFlatH.keys():
		
		if chrom not in exonH:
			exonH[chrom] = []

		for tH in refFlatH[chrom]:

			for i in range(len(tH['exnList'])):
				exonH[chrom].append(tH['exnList'][i])

	kgH = mygenome.loadKgByChr()

	for chrom in kgH.keys():
		
		if chrom not in exonH:
			exonH[chrom] = []

		for tH in kgH[chrom]:

			for i in range(len(tH['exnList'])):
				exonH[chrom].append(tH['exnList'][i])

		exonH[chrom] = list(set(exonH[chrom]))

		exonH[chrom].sort(lambda x,y: cmp(x[1],y[1]))
		exonH[chrom].sort(lambda x,y: cmp(x[0],y[0]))

	return exonH


def exonInclusion(chrom,chrSta,chrEnd):

	for (exnS,exnE) in exonH[chrom]:

		if exnS <= chrSta and chrEnd <= exnE:
			return True
		elif chrEnd <= exnS:
			break
	
	return False


def main(overlap=10,minNReads=1, inFileN='', outFileN=''):
	inFile = sys.stdin
	if inFileN != '':
		inFile = open(inFileN, 'r')
	outFile = sys.stdout
	if outFileN != '':
		outFile = open(outFileN, 'w')

	for line in inFile:

		sampN,loc,exn,cnt = line.split('\t')
		chrom,pos = loc.split(':')
		strand = exn[0]

		if int(cnt)<minNReads:
			continue
			
		if (strand=='+' and not exonInclusion(chrom,int(pos),int(pos)+overlap)) or (strand=='-' and not exonInclusion(chrom,int(pos)-overlap,int(pos))):
			outFile.write(line)
	outFile.flush()
	outFile.close()

exonH = loadExonH()
if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:s:',[])
	optH = mybasic.parseParam(optL)


	main(10,1)
