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

main('/EQL1/PrimRecur/signif/signif_mutation_normal.txt','/EQL1/PrimRecur/signif/signif_mutation_rsq.txt','/EQL1/PrimRecur/signif/signif_mutation.txt')
