#!/usr/bin/python

import sys, getopt, re
import mybasic, mygsnap, mygenome


def gsnap_process_junction(inGsnapFileName,outGsnapFileName,outReportFileName):

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

		transcript1 = re.search('label_[12]:([^,\t]*)', match.segL[0][3])
		gene1 = set()

		if transcript1:

			transcript1 = tuple([x.split('.exon')[0] for x in transcript1.group(1).split('|')])

			for t in transcript1:

				g = mygenome.gene(t,geneNameH,geneSetH,geneInfoH)

				if g.geneName:
					gene1.add(g.geneName)

		else:

			transcript1 = ()

		transcript2 = re.search('label_[12]:([^,\t]*)', match.segL[1][3])
		gene2 = set()

		if transcript2:

			transcript2 = tuple([x.split('.exon')[0] for x in transcript2.group(1).split('|')])

			for t in transcript2:

				g = mygenome.gene(t,geneNameH,geneSetH,geneInfoH)

				if g.geneName:
					gene2.add(g.geneName)

		else:

			transcript2 = ()

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

		bp_gene1 = mygenome.locus('%s:%s-%s%s' % (bp1.group(2),int(bp1.group(3))-1,bp1.group(3),trans_strand1)).overlappingGeneL(refFlatH=refFlatH,strand_sensitive=True)
		bp_gene2 = mygenome.locus('%s:%s-%s%s' % (bp2.group(2),int(bp2.group(3))-1,bp2.group(3),trans_strand2)).overlappingGeneL(refFlatH=refFlatH,strand_sensitive=True)

		if direction=='sense':
			key = (bp1.groups()[1:],bp2.groups()[1:])
			transcript = (transcript1,transcript2)
			gene = (tuple(gene1),tuple(gene2))
			bp_gene = (bp_gene1,bp_gene2)
		elif direction=='antisense':
			key = (bp2.groups()[1:],bp1.groups()[1:])
			transcript = (transcript2,transcript1)
			gene = (tuple(gene2),tuple(gene1))
			bp_gene = (bp_gene2,bp_gene1)
		else:
			raise Exception

		if key in juncHH:

			juncHH[key]['match'].append(r)
			juncHH[key]['seq'].append(r.seq())
			juncHH[key]['reg'].append((direction,offset))

		else:

			juncHH[key] = {'match':[r], 'splice_type':splice_type, 'seq':[r.seq()], 'reg':[(direction,offset)], 'transcript':transcript, 'gene':gene, 'bp_gene':bp_gene}

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

		for geneName in juncH['gene'][0]:
			gene = mygenome.gene(geneName,geneNameH,geneSetH,geneInfoH)
			geneInfo1.append('%s:%s:%s' % (geneName,gene.getAttr('desc'),gene.getAttr('summary')))
			censusInfo1.append('%s:%s:%s:%s' % (gene.getAttr('census_somatic'),gene.getAttr('census_germline'),gene.getAttr('census_mutType'),gene.getAttr('census_translocPartners')))

		geneInfo2 = []
		censusInfo2 = []

		for geneName in juncH['gene'][1]:
			gene = mygenome.gene(geneName,geneNameH,geneSetH,geneInfoH)
			geneInfo2.append('%s:%s:%s' % (geneName,gene.getAttr('desc'),gene.getAttr('summary')))
			censusInfo2.append('%s:%s:%s:%s' % (gene.getAttr('census_somatic'),gene.getAttr('census_germline'),gene.getAttr('census_mutType'),gene.getAttr('census_translocPartners')))

		outReportFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
			(type, juncH['splice_type'], ':'.join(key[0]), ':'.join(key[1]), \
			';'.join(juncH['transcript'][0]), ';'.join(juncH['transcript'][1]), ';'.join(juncH['gene'][0]), ';'.join(juncH['gene'][1]), ';'.join(geneInfo1), ';'.join(geneInfo2), \
			';'.join(censusInfo1), ';'.join(censusInfo2), ','.join(juncH['bp_gene'][0]), ','.join(juncH['bp_gene'][1]), \
			len(juncH['match']) ,len(set(juncH['seq'])), len(set(juncH['reg']))))

		for m in juncH['match']:
			outGsnapFile.write(m.rawText()+'\n')

# outGsnapFile: gsnap file sorted by junction frequency in reverse order

optL, argL = getopt.getopt(sys.argv[1:],'i:o:r:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:

	gsnap_process_junction(optH['-i'],optH['-o'],optH['-r'])
