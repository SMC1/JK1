#!/usr/bin/python

import sys, getopt, re
import mybasic, mygenome


def gene_annot(inReportFileName,outReportFileName):

	geneDB = mygenome.getGeneDB()
	
	outReportFile = open(outReportFileName,'w')

	inFile = open(inReportFileName)

	header = inFile.readline()[:-1]

	outReportFile.write('%s\tgeneInfo\tcensus\tGO\tKEGG\tBiocarta\n' % header)

	for line in inFile:

		tokL = line[:-1].split('\t')
		geneName = tokL[0]

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

		outReportFile.write('%s\t%s\t%s\t%s\t%s\t%s\n' % \
			('\t'.join(tokL), ';'.join(geneInfo),';'.join(censusInfo), \
			';'.join(map(str,goInfoS)), ';'.join(map(str,keggInfoS)),';'.join(map(str,biocInfoS))))

gene_annot('/EQL1/PrimRecur/paired/DEG_RPKM.txt','/EQL1/PrimRecur/paired/DEG_RPKM_annot.txt')
