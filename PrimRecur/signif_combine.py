#!/usr/bin/python

import sys

def main(inFileN_xsq,inFileN_rsq,outFileN):

	f = open(inFileN_xsq)
	h = f.readline()

	xH = {}

	for l in f:
		tL = l[:-1].split('\t')
		xH[(tL[1],tL[2])] = l

	f = open(inFileN_rsq)
	h = f.readline()

	rH = {}

	for l in f:
		tL = l[:-1].split('\t')
		rH[(tL[1],tL[2])] = l

	outFile = open(outFileN,'w')
	outFile.write(h)

	kL = list(set(xH.keys() + rH.keys()))

	for k in kL:

		try:
			outFile.write(xH[k])
		except:
			outFile.write(rH[k])

	outFile.close()

#inDir = '/EQL1/PrimRecur/signif_20140107/'
#inDir = '/EQL1/PrimRecur/signif_20140121/'
#inDir = '/EQL1/PrimRecur/signif_20140204/'
inDir = '/EQL1/PrimRecur/signif_20140214/'
main(inDir + 'signif_mutation_normal.txt',inDir + 'signif_mutation_rsq.txt', inDir + 'signif_mutation_pre.txt')
