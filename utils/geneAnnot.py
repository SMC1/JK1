#!/usr/bin/python

import sys, getopt, re
import mybasic, mygenome


def gene_annot(geneN_idx=0, inFileN = '', outFileN = '', have_header=True):

	geneDB = mygenome.getGeneDB()
	
	inFile = sys.stdin
	if inFileN != '':
		inFile = open(inFileN, 'r')
	outFile = sys.stdout
	if outFileN != '':
		outFile = open(outFileN, 'w')

	if have_header:
		header = inFile.readline()[:-1]
		outFile.write('%s\tgeneInfo\tcensus\tGO\tKEGG\tBiocarta\n' % header)
	else:
		last_pos = inFile.tell() # remember current position
		header = inFile.readline().rstrip()
		ncol = len(header.split('\t'))
		headerL = map(lambda x: 'X%s' % (x + 1), range(ncol))
		outFile.write('%s\tgeneInfo\tcensus\tGO\tKEGG\tBiocarta\n' % '\t'.join(headerL))
		inFile.seek(last_pos) # return to original position
	#if have_header

	for line in inFile:

		tokL = line[:-1].split('\t')
		geneName = tokL[geneN_idx].split(',')[0]

		geneS = set()
		geneH = {}

		geneInfo = []
		censusInfo = []

		goInfoS = set()
		keggInfoS = set()
		biocInfoS = set()

		gene = mygenome.gene(geneName,geneDB=geneDB)

		geneInfo.append('%s:%s:%s' % (geneName,gene.getAttr('desc'),gene.getAttr('summary')))
		censusInfo.append('%s:%s:%s:%s' % (gene.getAttr('census_somatic'),gene.getAttr('census_germline'),gene.getAttr('census_mutType'),gene.getAttr('census_translocPartners')))

		goInfoS = goInfoS.union(set(gene.getAttr('go')))
		keggInfoS = keggInfoS.union(set(gene.getAttr('kegg')))
		biocInfoS = biocInfoS.union(set(gene.getAttr('biocarta')))

		outFile.write('%s\t%s\t%s\t%s\t%s\t%s\n' % \
			('\t'.join(tokL), ';'.join(geneInfo),';'.join(censusInfo), \
			';'.join(map(str,goInfoS)), ';'.join(map(str,keggInfoS)),';'.join(map(str,biocInfoS))))
	outFile.flush()
	outFile.close()
	inFile.close()

optL, argL = getopt.getopt(sys.argv[1:],'i:o:t',['no_header'])

optH = mybasic.parseParam(optL)
header = True
if '--no_header' in optH:
	header = False

if '-i' in optH:
	gene_annot(int(optH['-i']), have_header=header)
else:
	gene_annot(have_header=header)
