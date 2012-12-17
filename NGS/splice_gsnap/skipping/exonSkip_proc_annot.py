#!/usr/bin/python

import sys, getopt, re
import mybasic, mygenome


def exonSkip_proc_annot(inReportFileName,outReportFileName,inCnaGctFileName=None):

	geneDB = mygenome.getGeneDB()
	frameInfoH = mygenome.getFrameInfoH()

	if inCnaGctFileName:
		cnaDB = mygenome.tcgaCnaDB(inCnaGctFileName)
	else:
		cnaDB = None

	outReportFile = open(outReportFileName,'w')

	for line in open(inReportFileName):

		(sampN,bp1,bp2,t1,t2,nmatch,nseq,nreg) = line[:-1].split('\t')

		if inCnaGctFileName:
			indivId = re.match('.*(TCGA-[0-9]{2}-[0-9]{4}).*',sampN).group(1)

		geneS = set()
		geneH = {}

		for tL in (t1,t2):

			for t in tL.split(','):

				ro = re.match('(.*)\.exon([0-9]*)/[0-9]*',t)

				t = ro.group(1)
				e = int(ro.group(2))

				mybasic.addHash(geneH,t,e)

				g = mygenome.gene(t,geneDB=geneDB)

				if g.geneName:
					geneS.add(g.geneName)

		frameL = []

		for transId in geneH:

			exnList = geneH[transId]

			if len(exnList) != 2:
				continue

			#exnList.sort()
			cons = mygenome.frameCons(transId,exnList[0], transId,exnList[1],frameInfoH)

			if cons:
				frameL.append('%s:%s' % (transId,cons))
			else:
				continue

		cnaInfo = []
		geneInfo = []
		censusInfo = []

		goInfoS = set()
		keggInfoS = set()
		biocInfoS = set()

		for geneName in geneS:

			gene = mygenome.gene(geneName,geneDB=geneDB)

			if cnaDB:
				cnaInfo.append('%s:%s' % (geneName,cnaDB.query(indivId,geneName)))

			geneInfo.append('%s:%s:%s' % (geneName,gene.getAttr('desc'),gene.getAttr('summary')))
			censusInfo.append('%s:%s:%s:%s' % (gene.getAttr('census_somatic'),gene.getAttr('census_germline'),gene.getAttr('census_mutType'),gene.getAttr('census_translocPartners')))

			goInfoS = goInfoS.union(set(gene.getAttr('go')))
			keggInfoS = keggInfoS.union(set(gene.getAttr('kegg')))
			biocInfoS = biocInfoS.union(set(gene.getAttr('bioc')))

		outReportFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
			(sampN, bp1,bp2, t1,t2, ','.join(frameL), ';'.join(geneS), ','.join(cnaInfo),';'.join(geneInfo),';'.join(censusInfo), \
			';'.join(map(str,goInfoS)), ';'.join(map(str,keggInfoS)),';'.join(map(str,biocInfoS)),nmatch,nseq,nreg))



optL, argL = getopt.getopt(sys.argv[1:],'i:o:c:',[])

optH = mybasic.parseParam(optL)

inFileName = optH['-i']
outFileName = optH['-o']

if '-c' in optH:
	exonSkip_proc_annot(inFileName,outFileName,optH['-c'])
else:
	exonSkip_proc_annot(inFileName,outFileName)
