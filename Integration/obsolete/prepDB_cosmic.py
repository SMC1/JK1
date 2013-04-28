#!/usr/bin/python

import sys, getopt, re, numpy
import mybasic

def main(inFileName,geneList=[]):

	dataH = {}

#	nameL = ('Mutation GRCh37 genome position', 'Mutation GRCh37 strand','Gene name','ID_sample','ID_tumour','Primary site', \
#		'Site subtype','Primary histology','Histology subtype','Genome-wide screen','Mutation ID','Mutation CDS','Mutation AA', \
#		'Mutation Description','Mutation zygosity','Mutation somatic status','Pubmed_PMID','Sample source','Tumor origin','Comments')

	nameL = ('Gene name','Mutation CDS','Mutation AA','Mutation Description','Mutation GRCh37 genome position','Mutation GRCh37 strand','Mutation somatic status')

	inFile = open(inFileName)

	headerL = inFile.readline()[:-1].split('\t')

	idxH = dict([(x, headerL.index(x)) for x in nameL])

	for line in inFile:

		valueL = line[:-1].split('\t')

		geneN = valueL[idxH['Gene name']]

		if len(geneList)>0 and geneN not in geneList:
			continue

		coord = valueL[idxH['Mutation GRCh37 genome position']]	

		if not coord:
			continue

		somatic = valueL[idxH['Mutation somatic status']]	

		if not 'somatic' in somatic:
			continue

		(chrNum,chrSta,chrEnd) = re.search('([^:-]+):([^:-]+)-([^:-]+)', coord).groups()

		cds = valueL[idxH['Mutation CDS']]	
		aa = valueL[idxH['Mutation AA']]	
		desc = valueL[idxH['Mutation Description']]	
		strand = valueL[idxH['Mutation GRCh37 strand']]	

		rm = re.match('c\.[_0-9]+([ATGC]*)>([ATGC]*)',cds)

		if rm:
			ref,alt = rm.groups()
		else:
			ref,alt = 'NULL','NULL'

		key = (chrNum,chrSta,chrEnd,strand,ref,alt)

		if key in dataH:
			mybasic.pushHash(dataH[key],'geneN',geneN)
			mybasic.pushHash(dataH[key],'cds',cds)
			mybasic.pushHash(dataH[key],'aa',aa)
			mybasic.pushHash(dataH[key],'desc',desc)
		else:
			dataH[key] = {'geneN':set([geneN]), 'cds':set([cds]), 'aa':set([aa]), 'desc':set([desc])}

	for ((chrNum,chrSta,chrEnd,strand,ref,alt),infoH) in dataH.iteritems():

		sys.stdout.write('chr%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (chrNum,chrSta,chrEnd,strand, ref,alt,\
			','.join(infoH['geneN']), ','.join(infoH['cds']), ','.join(infoH['aa']), ','.join(infoH['desc'])))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#	main(optH['-i'], optH['-o'])

#main('/data1/Sequence/cosmic/CosmicCompleteExport_v63_300113.tsv',['EGFR'])
main('/data1/Sequence/cosmic/CosmicCompleteExport_v63_300113.tsv')
