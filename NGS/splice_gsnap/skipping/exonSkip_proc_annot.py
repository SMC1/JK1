#!/usr/bin/python

import sys, getopt, re
import mybasic, mygenome


# not yet modified for exon skipping

def gsnap_process_junction(inReportFileName,outReportFileName):

	geneDB = mygenome.getGeneDB()

	outReportFile = open(outReportFileName,'w')

	for line in open(inReportFileName):

		(sampN,bp1,bp2,t1,t2,nmatch,nseq,nreg) = line[:-1].split('\t')

		geneS = set()

		for tL in (t1,t2):

			for t in tL.split('|'):

				t = t.split('.exon')[0]

				g = mygenome.gene(t,geneDB=geneDB)

				if g.geneName:
					geneS.add(g.geneName)

		geneInfo = []
		censusInfo = []

		for geneName in geneS:
			gene = mygenome.gene(geneName,geneDB=geneDB)
			geneInfo.append('%s:%s:%s' % (geneName,gene.getAttr('desc'),gene.getAttr('summary')))
			censusInfo.append('%s:%s:%s:%s' % (gene.getAttr('census_somatic'),gene.getAttr('census_germline'),gene.getAttr('census_mutType'),gene.getAttr('census_translocPartners')))
			goInfo = gene.getAttr('go')
			keggInfo = gene.getAttr('kegg')
			biocartaInfo = gene.getAttr('biocarta')

		outReportFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
			(sampN, bp1,bp2, t1,t2, ';'.join(geneS),';'.join(geneInfo),';'.join(censusInfo),';'.join(map(str,goInfo)), ';'.join(map(str,keggInfo)),';'.join(map(str,biocartaInfo)),nmatch,nseq,nreg))


# outGsnapFile: gsnap file sorted by junction frequency in reverse order

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:
		gsnap_process_junction(optH['-i'],optH['-o'])
