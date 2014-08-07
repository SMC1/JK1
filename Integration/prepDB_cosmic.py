#!/usr/bin/python

import sys, re, os
from glob import glob

def parse_info(info):
	itemL = info.split(';')
	datH = {}
	for item in itemL:
		tag = item.split('=')[0]
		val = '='.join(item.split('=')[1:])
		datH[tag] = val
	return(datH)

def prep_cosmic(cosmicVCF, inFileNL, outFileN, geneList=[]):
	os.system('date')
	mutH = prep_cosmic_vcf(cosmicVCF, geneList)
	os.system('date')
	prep_cosmic_csv(mutH, inFileNL, outFileN, geneList)

def prep_cosmic_vcf(cosmicVCF, geneList=[]):
	dataH = {}
	inFile = open(cosmicVCF)
	for line in inFile:
		if line[0] == '#':
			continue
		
		colL = line.rstrip().split('\t')
		chr = colL[0]
		pos = int(colL[1])
		ref = colL[3]
		alt = colL[4]

		infoH = parse_info(colL[7])
		if 'STRAND' not in infoH or 'CDS' not in infoH or 'AA' not in infoH:
			continue
		gene = infoH['GENE']
		if len(geneList)>0 and gene not in geneList:
			continue
		cds = infoH['CDS']
		aa = infoH['AA']

		dataH[(gene,cds,aa)] = (chr,pos,ref,alt)
	##for line
	return(dataH)

def prep_cosmic_csv(dataH, inFileNL, outFileN, geneList=[]):
	mutH = {}
	cnt = len(inFileNL)
	for inFileN in inFileNL:
		gene = re.match('(.*).csv', os.path.basename(inFileN)).group(1)
		idx = inFileNL.index(inFileN)
		if idx % 10 == 9:
			print '%s/%s' % (idx, cnt)
			print os.system('date')

		inFile = open(inFileN)
		for i in range(7):
			inFile.readline()
		headerL = inFile.readline().rstrip().split(',')
		for line in inFile:
			colL = line.rstrip().split(',')

			samp_id = colL[headerL.index('Sample Name')]
			aa = colL[headerL.index('Amino Acid')]
			cds = colL[headerL.index('Nucleotide')]
			tissue = colL[headerL.index('Primary Tissue')]
			status = colL[headerL.index('Somatic Status')]

			pos = colL[headerL.index('Genome Start GRCh37')]
			chr = colL[headerL.index('Chromosome GRCh37')]

			if 'Somatic' not in status or (gene, cds, aa) not in dataH:
				continue

			locus = dataH[(gene,cds,aa)]
			if locus not in mutH:
				mutH[locus] = {}
			if tissue not in mutH[locus]:
				mutH[locus][tissue] = set()
			mutH[locus][tissue].add(samp_id)

		#for line
	#for inFileN

	outFile = open(outFileN, 'w')
	for var in mutH:
		outFile.write('chr%s\t%s\t%s\t%s' % var)
		cntL = []
		for tissue in mutH[var]:
			cntL += ['%s:%s' % (tissue, len(mutH[var][tissue]))]
		outFile.write('\t%s\n' % ';'.join(cntL))
	#for var
	outFile.flush()
	outFile.close()

#['Sample Name', 'COSMIC Sample ID', 'Amino Acid', 'Nucleotide', 'Primary Tissue', 'Tissue subtype 1', 'Tissue subtype 2', 'Histology', 'Histology subtype 1', 'Histology subtype 2', 'Pubmed ID', 'studies', 'Mutation ID', 'Somatic Status', 'Sample Source', 'Zygosity', 'Chromosome NCBI36', 'Genome Start NCBI36', 'Genome Stop NCBI36', 'Chromosome GRCh37', 'Genome Start GRCh37', 'Genome Stop GRCh37']

if __name__ == '__main__':
	prep_cosmic('/data1/Sequence/cosmic/v69/CosmicCodingMuts.vcf', glob('/data1/Sequence/cosmic/v69/genes/*/*.csv'), '/data1/Sequence/cosmic/cosmic_confirmed_v69.dat')
	if os.path.isfile('/data1/Sequence/cosmic/cosmic_confirmed.dat'):
		os.system('unlink /data1/Sequence/cosmic/cosmic_confirmed.dat')
	os.system('ln -s /data1/Sequence/cosmic/cosmic_confirmed_v69.dat /data1/Sequence/cosmic/cosmic_confirmed.dat')
