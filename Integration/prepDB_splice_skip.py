#!/usr/bin/python

import sys, getopt, re
import mybasic

def parse(exon1,exon2):

	h = {}

	for t in exon1.split(','):

		rm = re.match('(.+)\.exon(.+)\/(.+)',t)
		h[(rm.group(1),int(rm.group(3)))] = [int(rm.group(2))]

	for t in exon2.split(','):

		rm = re.match('(.+)\.exon(.+)\/(.+)',t)

		if (rm.group(1),int(rm.group(3))) in h:
			h[(rm.group(1),int(rm.group(3)))].append(int(rm.group(2)))

	h2 = {}

	for t in h:
		
		if len(h[t]) == 2:
			mybasic.addHash(h2,tuple(h[t]),t)

	h2_items = h2.items()
	h2_items.sort(lambda x,y: cmp(len(y[1]),len(x[1])))

	return ','.join(['%s-%s' % (eS+1,eE-1) for ((eS,eE),l) in h2_items])
	#return ','.join(['%s-%s:%s' % (eS+1,eE-1,l) for ((eS,eE),l) in h2.iteritems()])

def main(inGctFileName,geneList=None):

	inFile = open(inGctFileName)

	headerL = inFile.readline()[:-1].split('\t')

	for line in inFile:

		dataL = line[:-1].split('\t')

		if geneList and dataL[5] in geneList:

			(sampN,loc1,loc2,geneN,exon1,exon2,frame,nPos) = (dataL[0],dataL[1],dataL[2],dataL[5],dataL[3],dataL[4],dataL[6],dataL[-1])

			sampN = re.search('[^L]?([0-9]{3})',sampN).group(1)

			parsed = parse(exon1,exon2)

			sys.stdout.write('S%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (sampN,loc1,loc2,geneN,frame,nPos,parsed,exon1,exon2))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#	main(optH['-i'], optH['-o'])

main('/EQL1/NSL/RNASeq/alignment/splice_skipping_NSL36.txt',['EGFR'])
