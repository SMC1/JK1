#!/usr/bin/python

import sys, getopt, re
import mybasic, mygenome


def gene_annot(inReportFileName,outReportFileName):

	geneDB = mygenome.getGeneDB()
	
	outReportFile = open(outReportFileName,'w')

	inFile = open(inReportFileName)

	header = inFile.readline()[:-1]

	outReportFile.write('%s\tgeneInfo\tcensus\tGO\tKEGG\tBiocarta\n' % header)

	headerL = header.split('\t')

	if 'geneN' in headerL:
		geneN_idx = headerL.index('geneN')

	if 'gene_symL' in headerL:
		geneN_idx = headerL.index('gene_symL')
	
	if 'SYMBOL' in headerL:
		geneN_idx = headerL.index('SYMBOL')

	for line in inFile:

		tokL = line[:-1].split('\t')
#		geneName = tokL[geneN_idx].split(',')[0]
		geneName = tokL[geneN_idx].split(';')[0]

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
if __name__ == '__main__':
	#gene_annot('/EQL1/PrimRecur/paired/DEG_RPKM.txt','/EQL1/PrimRecur/paired/DEG_RPKM_annot.txt')
	#gene_annot('/EQL2/SGI_20131031/RNASeq/results/DEG_RPKM.txt','/EQL2/SGI_20131031/RNASeq/results/DEG_RPKM_annot.txt')
	#gene_annot('/EQL1/PrimRecur/signif/signif_mutation_stat.txt','/EQL1/PrimRecur/signif/signif_mutation_stat_annot.txt')
	#gene_annot('/EQL3/pipeline/somatic_mutect/signif_mutect_somatic_stat.txt','/EQL3/pipeline/somatic_mutect/signif_mutect_somatic_stat_annot.txt')
	#gene_annot('/EQL1/PrimRecur/signif_20140107/signif_mutation_stat.txt','/EQL1/PrimRecur/signif_20140107/signif_mutation_stat_annot.txt')
	#gene_annot('/EQL1/PrimRecur/signif_20140121/signif_mutation_stat.txt','/EQL1/PrimRecur/signif_20140121/signif_mutation_stat_annot.txt')
	#gene_annot('/EQL1/PrimRecur/signif_20140204/signif_mutation_stat.txt','/EQL1/PrimRecur/signif_20140204/signif_mutation_stat_annot.txt')
	gene_annot('/EQL1/PrimRecur/signif_20140214/signif_mutation_stat.txt','/EQL1/PrimRecur/signif_20140214/signif_mutation_stat_annot.txt')
