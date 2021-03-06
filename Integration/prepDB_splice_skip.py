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


def main(inFileName,minNPos,sampNamePat=('(.*)',''),geneList=[], outFileName=''):

	inFile = open(inFileName)
	outFile = sys.stdout
	if outFileName != '':
		outFile = open(outFileName,'w')

	headerL = inFile.readline()[:-1].split('\t')

	for line in inFile:

		dataL = line[:-1].split('\t')

		if geneList==[] or dataL[5] in geneList:

			(sampN,loc1,loc2,geneN,exon1,exon2,frame,nReads,nPos) = (dataL[0],dataL[1],dataL[2],dataL[5],dataL[3],dataL[4],dataL[6],dataL[-3],dataL[-1])

			if int(nPos) < minNPos:
				continue

			sampN = re.search(sampNamePat[0],sampN).group(1).replace('.','_').replace('-','_')

			parsed = parse(exon1,exon2)

			outFile.write('%s%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (sampNamePat[1],sampN,loc1,loc2,geneN,frame,parsed,exon1,exon2,nReads,nPos))
	outFile.flush()
	outFile.close()

if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

	optH = mybasic.parseParam(optL)

	#if '-i' in optH and '-o' in optH:
	#	main(optH['-i'], optH['-o'])

	#main('/EQL1/NSL/RNASeq/alignment/splice_skipping_NSL36.txt',5,('[^L]?([0-9]{3})','S'))
	#main('/EQL3/TCGA/GBM/RNASeq/alignment/splice_skipping_170.txt',5,('.*(TCGA-..-....).*',''))
	#main('/EQL2/TCGA/LUAD/RNASeq/skipping/splice_skip_EGFR_TCGA_LUAD.txt',1,('.*(TCGA-..-....-...).*',''))
	#main('/EQL1/NSL/RNASeq/results/exonSkip/splice_skip_NSL45.txt',1,('([0-9]{3})','S'))
	#main('/EQL2/SGI_20131031/RNASeq/results/exonSkip/splice_skip_30.txt',1,('.{1}(.*)_RSq','S'))
	#main('/EQL1/NSL/RNASeq/results/exonSkip/splice_skip_SGI20131119_6.txt',1,('.{1}(.*)_RSq','S'))
	main('/EQL1/NSL/RNASeq/results/exonSkip/splice_skip_SGI20131212_6.txt',1,('.{1}(.*)_RSq','S'))
