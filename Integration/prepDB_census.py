#!/usr/bin/python

import sys, getopt, re, numpy
import mybasic

def main(inFileName,geneList=[]):

	nameL = ('Symbol','Name','Chr','Cancer Somatic Mut','Cancer Germline Mut','Tumour Types  (Somatic Mutations)','Tumour Types (Germline Mutations)','Cancer Syndrome','Mutation Type','Translocation Partner')

	inFile = open(inFileName)

	headerL = inFile.readline()[:-1].split('\t')

	idxH = dict([(x, headerL.index(x)) for x in nameL])

	for line in inFile:

		valueL = line[:-1].split('\t')

		geneN = valueL[idxH['Symbol']]

		if len(geneList)>0 and geneN not in geneList:
			continue

		sys.stdout.write('%s\t%s\tchr%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
			(geneN, valueL[idxH['Name']], valueL[idxH['Chr']], \
			('y' if valueL[idxH['Cancer Somatic Mut']] else ''), ('y' if valueL[idxH['Cancer Germline Mut']] else ''), \
			valueL[idxH['Tumour Types  (Somatic Mutations)']], valueL[idxH['Tumour Types (Germline Mutations)']], \
			valueL[idxH['Cancer Syndrome']], valueL[idxH['Mutation Type']], valueL[idxH['Translocation Partner']]))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#	main(optH['-i'], optH['-o'])

main('/data1/Sequence/geneinfo/cancer_gene_census.tsv')
