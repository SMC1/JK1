#!/usr/bin/python

# for firehose MAF data

import sys, getopt, re, numpy
import mybasic

def main(inFileName,geneList=[]):

	nameL = ('Hugo_Symbol','NCBI_Build','Chromosome','Start_position','End_position','Strand','Variant_Classification','Variant_Type','Reference_Allele', \
		'Tumor_Seq_Allele1','Tumor_Sample_Barcode','Mutation_Status','Transcript_Strand','cDNA_Change','Protein_Change', 'Alternative_allele_reads_count','Reference_allele_reads_count', \
		'COSMIC_overlapping_mutations','MUTSIG_Published_Results')

	inFile = open(inFileName)

	headerL = inFile.readline()[:-1].split('\t')

	idxH = dict([(x, headerL.index(x)) for x in nameL if x in headerL])

	for line in inFile:

		if line[0]== '#':
			continue

		valueL = line[:-1].split('\t')

		geneN = valueL[idxH['Hugo_Symbol']]

		if len(geneList)>0 and geneN not in geneList:
			continue

		if valueL[idxH['NCBI_Build']] != '37' or valueL[idxH['Strand']] != '+':
			print 'Invalid entry: %s' % line,
			sys.exit(1)

		chrNum = valueL[idxH['Chromosome']]	
		chrSta = valueL[idxH['Start_position']]	
		chrEnd = valueL[idxH['End_position']]	

		ref = valueL[idxH['Reference_Allele']]	
		alt = valueL[idxH['Tumor_Seq_Allele1']]	

		count_ref = valueL[idxH['Reference_allele_reads_count']]	
		count_alt = valueL[idxH['Alternative_allele_reads_count']]	

		strand = valueL[idxH['Transcript_Strand']]	

		cds = valueL[idxH['cDNA_Change']]	
		aa = valueL[idxH['Protein_Change']]	

		desc = '%s:%s' % (valueL[idxH['Variant_Type']], valueL[idxH['Variant_Classification']])

		if 'Silent' in desc:
			continue

		if 'COSMIC_overlapping_mutations' in idxH:
			cosmic = valueL[idxH['COSMIC_overlapping_mutations']]
		else:
			cosmic = ''

		if 'MUTSIG_Published_Results' in idxH:
			mutsig = valueL[idxH['MUTSIG_Published_Results']]
		else:
			mutsig = ''

#		sampId = re.match('.*(TCGA-..-....).*',valueL[idxH['Tumor_Sample_Barcode']]).group(1)
		sampId = valueL[idxH['Tumor_Sample_Barcode']]

		key = (sampId,chrNum,chrSta,chrEnd,strand,ref,alt)

		sys.stdout.write('%s\tchr%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
			(sampId, chrNum,chrSta,chrEnd, ref,alt, count_ref,count_alt, strand, \
			geneN, cds, aa, desc, cosmic, mutsig))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#	main(optH['-i'], optH['-o'])

main('/data1/CCLE_Sanger/CCLE_hybrid_capture1650_hg19_NoCommonSNPs_NoNeutralVariants_CDS_2012.05.07.maf')
#main('/EQL1/TCGA/GBM/mutation/GBM-TP.final_analysis_set.maf')
