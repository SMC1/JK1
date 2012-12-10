#!/usr/bin/python

import sys, getopt, re
import mybasic, mygsnap, mygenome


def gsnap_process_junction(inGsnapFileName,outGsnapFileName,outReportFileName,sampN):

	geneNameH = mygenome.geneNameH()
	geneSetH = mygenome.geneSetH()
	geneInfoH = mygenome.geneInfoH(geneNameH,geneSetH)
	refFlatH = mygenome.loadRefFlatByChr()

	result = mygsnap.gsnapFile(inGsnapFileName,False)

	juncHH = {}

	for r in result:

		match = r.matchL()[0]

		if not '(transloc)' in r.pairRel:
			raise Exception

		if len(match.segL) != 2:
			raise Exception

		splice_type = re.search('splice_type:([^,\t]*)', match.segL[0][3]).group(1)
		direction = re.search('dir:([^,\t]*)', match.segL[0][3]).group(1)
		offset = int(re.search('\.\.([0-9]*)', match.segL[0][1]).group(1))

		rm = re.search('label_[12]:([^,\t]*)', match.segL[0][3])
		gene1 = set()

		if rm:

			trans_exon1 = rm.group(1).split('|')

			for t in trans_exon1:

				g = mygenome.gene(t.split('.exon')[0],geneNameH,geneSetH,geneInfoH)

				if g.geneName:
					gene1.add(g.geneName)

		else:

			trans_exon1 = ()

		rm = re.search('label_[12]:([^,\t]*)', match.segL[0][3])
		gene2 = set()

		if rm:

			trans_exon2 = rm.group(1).split('|')

			for t in trans_exon2:

				g = mygenome.gene(t.split('.exon')[0],geneNameH,geneSetH,geneInfoH)

				if g.geneName:
					gene2.add(g.geneName)

		else:

			trans_exon2 = ()


		s1 = match.segL[0][2]
		s2 = match.segL[1][2]

		bp1 = re.match('([+-])([^:]+):[0-9]+..([0-9]+)',s1)
		bp2 = re.match('([+-])([^:]+):([0-9]+)..[0-9]+',s2)

		if (bp1.group(1),direction) in (('+','sense'),('-','antisense')):
			trans_strand1 = '+'
		elif (bp1.group(1),direction) in (('+','antisense'),('-','sense')):
			trans_strand1 = '-'
		else:
			raise Exception

		if (bp2.group(1),direction) in (('+','sense'),('-','antisense')):
			trans_strand2 = '+'
		elif (bp2.group(1),direction) in (('+','antisense'),('-','sense')):
			trans_strand2 = '-'
		else:
			raise Exception

		locus1 = mygenome.locus('%s:%s-%s%s' % (bp1.group(2),int(bp1.group(3))-1,bp1.group(3),trans_strand1))
		bp_gene1 = list(set(locus1.overlappingGeneL(refFlatH=refFlatH,strand_sensitive=True)).difference(gene1))

		locus2 = mygenome.locus('%s:%s-%s%s' % (bp2.group(2),int(bp2.group(3))-2,bp2.group(3),trans_strand2))
		bp_gene2 = list(set(locus2.overlappingGeneL(refFlatH=refFlatH,strand_sensitive=True)).difference(gene2))

		if direction=='sense':
			key = (bp1.groups()[1:],bp2.groups()[1:])
			trans_exon = (trans_exon1,trans_exon2)
			gene = (list(gene1),list(gene2))
			bp_gene = (bp_gene1,bp_gene2)
		elif direction=='antisense':
			key = (bp2.groups()[1:],bp1.groups()[1:])
			trans_exon = (trans_exon2,trans_exon1)
			gene = (list(gene2),list(gene1))
			bp_gene = (bp_gene2,bp_gene1)
		else:
			raise Exception

		if key in juncHH:

			juncHH[key]['match'].append(r)
			juncHH[key]['seq'].append(r.seq())
			juncHH[key]['reg'].append((direction,offset))

		else:

			juncHH[key] = {'match':[r], 'splice_type':splice_type, 'seq':[r.seq()], 'reg':[(direction,offset)], 'trans_exon':trans_exon, 'gene':gene, 'bp_gene':bp_gene}

	juncKH = juncHH.items()
	juncKH.sort(lambda x,y: cmp(len(set(y[1]['reg'])),len(set(x[1]['reg']))))

	outGsnapFile = open(outGsnapFileName,'w')
	outReportFile = open(outReportFileName,'w')

	for (key, juncH) in juncKH:

		if key[0][0] == key[1][0]:
			type = 'intra'
		else:
			type = 'inter'

		geneInfo1 = []
		censusInfo1 = []

		for geneName in juncH['gene'][0]+juncH['bp_gene'][0]:
			gene = mygenome.gene(geneName,geneNameH,geneSetH,geneInfoH)
			geneInfo1.append('%s:%s:%s' % (geneName,gene.getAttr('desc'),gene.getAttr('summary')))
			censusInfo1.append('%s:%s:%s:%s' % (gene.getAttr('census_somatic'),gene.getAttr('census_germline'),gene.getAttr('census_mutType'),gene.getAttr('census_translocPartners')))

		geneInfo2 = []
		censusInfo2 = []

		for geneName in juncH['gene'][1]+juncH['bp_gene'][1]:
			gene = mygenome.gene(geneName,geneNameH,geneSetH,geneInfoH)
			geneInfo2.append('%s:%s:%s' % (geneName,gene.getAttr('desc'),gene.getAttr('summary')))
			censusInfo2.append('%s:%s:%s:%s' % (gene.getAttr('census_somatic'),gene.getAttr('census_germline'),gene.getAttr('census_mutType'),gene.getAttr('census_translocPartners')))

		outReportFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s;%s\t%s;%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
			(type, juncH['splice_type'], sampN, ':'.join(key[0]), ':'.join(key[1]), \
			','.join(juncH['trans_exon'][0]), ','.join(juncH['trans_exon'][1]), \
			','.join(juncH['gene'][0]), ','.join(juncH['bp_gene'][0]), ','.join(juncH['gene'][1]), ','.join(juncH['bp_gene'][1]), \
			';'.join(geneInfo1), ';'.join(geneInfo2), ';'.join(censusInfo1), ';'.join(censusInfo2), \
			len(juncH['match']) ,len(set(juncH['seq'])), len(set(juncH['reg']))))

		for m in juncH['match']:
			outGsnapFile.write(m.rawText()+'\n')

# outGsnapFile: gsnap file sorted by junction frequency in reverse order

optL, argL = getopt.getopt(sys.argv[1:],'i:o:r:s:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:

	if '-s' in optH:
		gsnap_process_junction(optH['-i'],optH['-o'],optH['-r'],optH['-s'])
	else:
		gsnap_process_junction(optH['-i'],optH['-o'],optH['-r'],optH['-i'])
