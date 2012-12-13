#!/usr/bin/python

import sys, getopt, re
import mybasic, mygsnap, mygenome


def fusion_proc_annot(inReportFileName,outReportFileName,inCnaGctFileName=None):

	geneDB = mygenome.getGeneDB()
	frameInfoH = mygenome.getFrameInfoH()
	refFlatH = mygenome.loadRefFlatByChr()

	if inCnaGctFileName:
		cnaDB = mygenome.tcgaCnaDB(inCnaGctFileName)
	else:
		cnaDB = None

	inReportFile = open(inReportFileName)
	outReportFile = open(outReportFileName,'w')

	for line in open(inReportFileName):

		(splice_type,sampN,bp1,bp2,teStr1,teStr2,nmatch,nseq,nreg) = line[:-1].split('\t')

		indivId = re.match('.*(TCGA-[0-9]{2}-[0-9]{4}).*',sampN).group(1)

		geneStatL = []

		for (bp,teStr) in ((bp1,teStr1),(bp2,teStr2)):

			geneS = set()
			teL = []

			for te in teStr.split(','):

				rm = re.match('(.*)\.exon([0-9]*)/[0-9]*',te)

				if rm:

					t = rm.group(1)
					e = int(rm.group(2))

					g = mygenome.gene(t,geneDB=geneDB)

					if g.geneName:
						geneS.add(g.geneName)

					teL.append((t,e))

			rm = re.match('([+-])(chr[^:]*):([0-9]*)',bp)

			bp_geneS = set(mygenome.locus('%s:%s-%s%s' % (rm.group(2),int(rm.group(3))-1,rm.group(3),rm.group(1))).overlappingGeneL(refFlatH=refFlatH,strand_sensitive=True))
			bp_geneS = bp_geneS.difference(geneS)

			cnaInfo = []
			geneInfo = []
			censusInfo = []

			goInfoS = set()
			keggInfoS = set()
			biocartaInfoS = set()

			for geneName in list(geneS) + list(bp_geneS):

				gene = mygenome.gene(geneName,geneDB=geneDB)

				if cnaDB:
					cnaInfo.append('%s:%s' % (geneName,cnaDB.query(indivId,geneName)))

				geneInfo.append('%s:%s:%s' % (geneName,gene.getAttr('desc'),gene.getAttr('summary')))
				censusInfo.append('%s:%s:%s:%s' % (gene.getAttr('census_somatic'),gene.getAttr('census_germline'),gene.getAttr('census_mutType'),gene.getAttr('census_translocPartners')))
				goInfoS = goInfoS.union(set(gene.getAttr('go')))
				keggInfoS = keggInfoS.union(set(gene.getAttr('kegg')))
				biocartaInfoS = biocartaInfoS.union(set(gene.getAttr('biocarta')))

			geneStatL.append((bp1.split(':')[0],bp,teStr,teL,geneS,bp_geneS,cnaInfo,geneInfo,censusInfo,goInfoS,keggInfoS,biocartaInfoS))


		(chrom1,bp1,teStr1,teL1,geneS1,bp_geneS1,cnaInfo1,geneInfo1,censusInfo1,goInfoS1,keggInfoS1,biocartaInfoS1) = geneStatL[0]
		(chrom2,bp2,teStr2,teL2,geneS2,bp_geneS2,cnaInfo2,geneInfo2,censusInfo2,goInfoS2,keggInfoS2,biocartaInfoS2) = geneStatL[1]


		if chrom1 == chrom2:
			type = 'intra'
		else:
			type = 'inter'


		frameL = []

		for (t1,e1) in teL1:

			for (t2,e2) in teL2:

				cons = mygenome.frameCons(t1,e1, t2,e2, frameInfoH)

				if cons=='Y':
					frameL.append('%s.%s-%s.%s:%s' % (t1,e1,t2,e2,cons))

		outReportFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
			(sampN, splice_type, type, bp1,bp2, teStr1,teStr2, ','.join(frameL), ','.join(cnaInfo1), ','.join(cnaInfo2), \
			'%s;%s' % (','.join(geneS1),','.join(bp_geneS1)), ';'.join(geneInfo1), ';'.join(censusInfo1), \
			';'.join(map(str,goInfoS1)), ';'.join(map(str,keggInfoS1)), ';'.join(map(str,biocartaInfoS1)), 
			'%s;%s' % (','.join(geneS2),','.join(bp_geneS2)), ';'.join(geneInfo2), ';'.join(censusInfo2), \
			';'.join(map(str,goInfoS2)), ';'.join(map(str,keggInfoS2)), ';'.join(map(str,biocartaInfoS2)), 
			nmatch,nseq,nreg))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:c:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:

	if '-c' in optH:
		fusion_proc_annot(optH['-i'],optH['-o'],optH['-c'])
	else:
		fusion_proc_annot(optH['-i'],optH['-o'])
