#!/usr/bin/python

import sys, getopt, re
import mybasic


def parse(juncInfo):

	geneL = []

	maxTrans = 0

	for junc in juncInfo.split(','):

		rm = re.match('([^:]+):[^:]+:(.*)\/(.*)',junc)
		geneL.append(rm.group(1))

		if int(rm.group(3)) > maxTrans:
			alias = '%s/%s' % (rm.group(2),rm.group(3))
			maxTrans = int(rm.group(3))

	return set(geneL), alias


def main(minNReads,geneList=[]):

	inFile = sys.stdin

	headerL = inFile.readline()[:-1].split('\t')

	for line in inFile:

		dataL = line[:-1].split('\t')

		(sampN,loc,juncInfo,nReads) = (dataL[0],dataL[1],dataL[2],dataL[3])

		if int(nReads) < minNReads:
			continue

		sampN = re.search('([0-9]{3})',sampN).group(1)

		geneS, alias = parse(juncInfo)

		if not geneList or geneS.intersection(geneList):
			sys.stdout.write('S%s\t%s\t%s\t%s\t%s\t%s\n' % (sampN, loc, ','.join(list(geneS)), juncInfo, alias, nReads))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#	main(optH['-i'], optH['-o'])

main(0)
