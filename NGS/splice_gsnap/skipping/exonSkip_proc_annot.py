#!/usr/bin/python

import sys, getopt, re
import mybasic, mygenome


def gsnap_process_junction(inReportFileName,outReportFileName):

	geneDB = mygenome.getGeneDB()
	frameInfoH = mygenome.getFrameInfoH()

	outReportFile = open(outReportFileName,'w')

	for line in open(inReportFileName):

		(sampN,bp1,bp2,t1,t2,nmatch,nseq,nreg) = line[:-1].split('\t')

		geneS = set()
		geneH = {}

		for tL in (t1,t2):

			for t in tL.split('|'):

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

			exnList.sort()
			cons = mygenome.frameCons(transId,exnList[0], transId,exnList[1],frameInfoH)

			if cons:
				frameL.append('%s:%s' % (transId,cons))
			else:
				continue

		geneInfo = []
		censusInfo = []

		for geneName in geneS:
			gene = mygenome.gene(geneName,geneDB=geneDB)
			geneInfo.append('%s:%s:%s' % (geneName,gene.getAttr('desc'),gene.getAttr('summary')))
			censusInfo.append('%s:%s:%s:%s' % (gene.getAttr('census_somatic'),gene.getAttr('census_germline'),gene.getAttr('census_mutType'),gene.getAttr('census_translocPartners')))
			goInfo = gene.getAttr('go')
			keggInfo = gene.getAttr('kegg')
			biocartaInfo = gene.getAttr('biocarta')

		outReportFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
			(sampN, bp1,bp2, t1,t2, ','.join(frameL),';'.join(geneS),';'.join(geneInfo),';'.join(censusInfo),';'.join(map(str,goInfo)), ';'.join(map(str,keggInfo)),';'.join(map(str,biocartaInfo)),nmatch,nseq,nreg))



optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:
	gsnap_process_junction(optH['-i'],optH['-o'])
