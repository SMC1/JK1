#!/usr/bin/python

# for firehose MAF data

import sys, getopt, re, os
import mybasic

def main(inDirName,inputFileName,inSnpDirName,geneList=[]):

	nameL = ('Chromosome', 'Position', 'Strand', 'Reference base', 'Alternate base', 'Sample ID', 'HUGO symbol', 'Amino acid change', 'AA change by COSMIC')
#
#	nameL = ('Hugo_Symbol','NCBI_Build','Chromosome','Start_position','End_position','Strand','Variant_Classification','Variant_Type','Reference_Allele', \
#		'Tumor_Seq_Allele1','Tumor_Seq_Allele1','Mutation_Status','Transcript_Strand','cDNA_Change','Protein_Change','COSMIC_overlapping_mutations','MUTSIG_Published_Results') 
#
	inputFileNL = os.listdir(inDirName)
	inputFileNL = filter(lambda x: re.match('(.*)_cravat.txt',x),inputFileNL)

	sampNL = list(set([re.match('(.*)_cravat.txt',inputFileN).group(1) for inputFileN in inputFileNL]))
	sampNL.sort()

	nameL2 = ('chrom','position','tumor_reads1','tumor_reads2','normal_reads1','normal_reads2','somatic_status')

	dataH = {}
	
	for inFileName in sampNL:

		inSnpFile = open('%s/%s.snp' %(inSnpDirName,inFileName))
		
		headerL = inSnpFile.readline()[:-1].split('\t')

		idxH = dict([(x, headerL.index(x)) for x in nameL2])
		
		for line in inSnpFile:

			valueL = line[:-1].split('\t')
			
			chrN = valueL[idxH['chrom']]
			pos = valueL[idxH['position']]
			
			status = valueL[idxH['somatic_status']]
		
			if status != 'Somatic':
				continue

			key = (inFileName,chrN,pos)
			
			n_ref_count = valueL[idxH['normal_reads1']]
			n_alt_count = valueL[idxH['normal_reads2']]
			
			t_ref_count = valueL[idxH['tumor_reads1']]
			t_alt_count = valueL[idxH['tumor_reads2']]
			
			dataH[key] = (n_ref_count,n_alt_count, t_ref_count,t_alt_count)

	inFile = open(inputFileName)

	for line in inFile:
		
		if line[0] == '#':
			continue
			
		headerL = line[:-1].split('\t')

		idxH = dict([(x, headerL.index(x)) for x in nameL])

		break
	
	for line in inFile:

		valueL = line[:-1].split('\t')

		fileId = valueL[idxH['Sample ID']]

		geneN = valueL[idxH['HUGO symbol']]

		if len(geneList)>0 and geneN not in geneList:
			continue

		if valueL[idxH['Strand']] != '+':
			print 'Invalid entry: %s' % line,
			sys.exit(1)

		chrNum = valueL[idxH['Chromosome']][3:]	
		chrSta = valueL[idxH['Position']]	
		chrEnd = valueL[idxH['Position']]	
			
		ref = valueL[idxH['Reference base']]	
		alt = valueL[idxH['Alternate base']]	

		count = dataH[(fileId,'chr%s' % chrNum,chrSta)]

		n_count_ref = count[0]	
		n_count_alt = count[1]	

		t_count_ref = count[2]	
		t_count_alt = count[3]	

		strand = valueL[idxH['Strand']]	

		cds = ''	
		aa = valueL[idxH['Amino acid change']]	

		if aa == 'No result':
			continue
		
		desc = ''

		if aa[0] == aa[-1]:
			desc = 'Silent'

		aa = 'p.%s' % aa

		if 'Silent' in desc or 'IGR' in desc:
			continue
			
		cosmic = valueL[idxH['AA change by COSMIC']]
		mutsig = ''

		if cosmic != '':
			cosmic = 'p.%s' % cosmic

		sampId = re.match('.*([0-9]{3}).*',fileId).group(1)
				
		key = (sampId,chrNum,chrSta,chrEnd,strand,ref,alt)
	
		sys.stdout.write('S%s\tchr%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
			(sampId, chrNum,chrSta,chrEnd, ref,alt, n_count_ref,n_count_alt, t_count_ref,t_count_alt, strand, \
			geneN, cds, aa, desc, cosmic,mutsig))


optL, argL = getopt.getopt(sys.argv[1:],'i:s:o:',[])

optH = mybasic.parseParam(optL)


main('/EQL1/NSL/exome_bam/mutation/cravat','/EQL1/NSL/exome_bam/mutation/cravat/NSL_GBM_24_cravat_output.tsv','/EQL1/NSL/exome_bam/mutation')
#main('/EQL1/TCGA/GBM/mutation/GBM-TP.final_analysis_set.maf')
