#!/usr/bin/python

import sys, getopt, re
import mybasic, mygsnap, mygenome


def gsnap_process_junction(inReportFileName,outReportFileName):

	geneNameH = mygenome.geneNameH()
	geneSetH = mygenome.geneSetH()
	geneInfoH = mygenome.geneInfoH(geneNameH,geneSetH)

	outReportFile = open(outReportFileName,'w')

	for line in open(inReportFileName):

		(spliceType,sampN,bp1,bp2,t1,t2,nmatch,nseq,nreg) = line[:-1].split('\t')

		gene1 = set()

		if t1:

			transcript1 = tuple(t1.split(';'))
	
			for t in transcript1:

				g = mygenome.gene(t,geneNameH,geneSetH,geneInfoH)

				if g.geneName:
					gene1.add(g.geneName)

		else:

			gene1 = ()

		gene2 = set()

		if t2:

			transcript2 = tuple(t2.split(';'))

			for t in transcript2:

				g = mygenome.gene(t,geneNameH,geneSetH,geneInfoH)

				if g.geneName:
					gene2.add(g.geneName)

		else:

			gene2 = ()

		bp_gene1 = set()

#		transcript1 = tuple([x for x in bp1.split('|') if "uc" in x])

		for t in tuple([x for x in bp1.split('|') if "uc" in x]):

			g = mygenome.gene(t,geneNameH,geneSetH,geneInfoH)

			if g.geneName:
				bp_gene1.add(g.geneName)
		
		bp_gene2 = set()

#		transcript2 = tuple([x for x in bp2.split('|') if "uc" in x])

		for t in tuple([x for x in bp2.split('|') if "uc" in x]):

			g = mygenome.gene(t,geneNameH,geneSetH,geneInfoH)

			if g.geneName:
				bp_gene2.add(g.geneName)

#		ch1 =  tuple([x for x in id1.split('|') if not "uc" in x])
#		ch2 =  tuple([x for x in id2.split('|') if not "uc" in x])


		if tuple([x for x in bp1.split('|') if "chr" in x])[0] == tuple([x for x in bp2.split('|') if "chr" in x])[0]:
			type = 'intra'
		else:
			type = 'inter'


		geneInfo1 = []
		censusInfo1 = []

		for geneName in gene1:
			gene = mygenome.gene(geneName,geneNameH,geneSetH,geneInfoH)
			geneInfo1.append('%s:%s:%s' % (geneName,gene.getAttr('desc'),gene.getAttr('summary')))
			censusInfo1.append('%s:%s:%s:%s' % (gene.getAttr('census_somatic'),gene.getAttr('census_germline'),gene.getAttr('census_mutType'),gene.getAttr('census_translocPartners')))

		geneInfo2 = []
		censusInfo2 = []

		for geneName in gene2:
			gene = mygenome.gene(geneName,geneNameH,geneSetH,geneInfoH)
			geneInfo2.append('%s:%s:%s' % (geneName,gene.getAttr('desc'),gene.getAttr('summary')))
			censusInfo2.append('%s:%s:%s:%s' % (gene.getAttr('census_somatic'),gene.getAttr('census_germline'),gene.getAttr('census_mutType'),gene.getAttr('census_translocPartners')))


		outReportFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
			(type, spliceType, sampN, bp1, bp2, \
			t1, t2, ';'.join(gene1), ';'.join(gene2), ';'.join(geneInfo1), ';'.join(geneInfo2), \
			';'.join(censusInfo1), ';'.join(censusInfo2), ','.join(bp_gene1), ','.join(bp_gene2), \
			nmatch ,nseq, nreg))



# outGsnapFile: gsnap file sorted by junction frequency in reverse order

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:

		gsnap_process_junction(optH['-i'],optH['-o'])
