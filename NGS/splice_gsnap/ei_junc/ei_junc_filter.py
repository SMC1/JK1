#!/usr/bin/python

import sys, getopt, re
import mybasic, mygsnap, mygenome


def loadRefFlatByChr():

	refFlatH = mygenome.loadRefFlatByChr()

	exonH = {}

	for chrom in refFlatH.keys():
		
		exonH[chrom] = []

		refFlatL = refFlatH[chrom]

		for tH in refFlatL:

			for i in range(len(tH['exnList'])):
				exonH[chrom].append(tH['exnList'][i])

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


def main(overlap=10):

	for line in sys.stdin:

		sampN,loc,exn,cnt = line.split('\t')
		chrom,pos = loc.split(':')
		strand = exn[0]

		if int(cnt)<=2:
			continue
			
		if (strand=='+' and not exonInclusion(chrom,int(pos),int(pos)+overlap)) or (strand=='-' and not exonInclusion(chrom,int(pos)-overlap,int(pos))):
			sys.stdout.write(line)


optL, argL = getopt.getopt(sys.argv[1:],'i:o:s:',[])
optH = mybasic.parseParam(optL)

exonH = loadRefFlatByChr()

main(10)
