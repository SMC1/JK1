#!/usr/bin/python

import os, sys, re
import fisher, math

TAG_KGP='KGPF'
TAG_ESP='ESPF'

def find_overlap_repeat(inFileN):
	repH = {}
 	for line in os.popen('bedtools intersect -u -a %s -b /data1/Sequence/ucsc_hg19/annot/simple.repeat.hg19.bed | cut -f 1,2,4,5' % inFileN).readlines():
		colL = line.rstrip().split('\t')
		chr = colL[0]
		pos = int(colL[1])
		ref = colL[2]
		alt = colL[3]
		repH[(chr,pos,ref,alt)] = 1
	##line
	return(repH)

def filter_indel_paired(inFileN, selectedFileN, outFileN, TH_FS_PVAL=0.1, TH_MAPQ=50, TH_MAPQ_A=30, TH_DP=10, TH_AD_A=5, TH_TFRAC=0.01, TH_POS_MED=10, TH_POS_MAD=3):
	repeatH = find_overlap_repeat(inFileN)
	inFile = open(inFileN)
	selectedFile = open(selectedFileN, 'w')
	outFile = open(outFileN, 'w')
	for line in inFile:
		if line[0] == '#':
			selectedFile.write(line)
			if line[2:12].lower() == 'fileformat':
				selectedFile.write('##INFO=<ID=T_FS_PVAL,Number=1,Type=Float,Description="p-value from Fisher\'s exact test of strand-bias">\n')
				selectedFile.flush()
			if line[:6].upper() == '#CHROM':
				colL = line.rstrip().split('\t')
				if '_B_' in colL[-1]: ## assume only 2 samples in the file
					tcol = len(colL)-2
					ncol = len(colL)-1
				else:
					tcol = len(colL)-1
					ncol = len(colL)-2
			continue
		colL = line.rstrip().split('\t')
		chr = colL[0]
		pos = int(colL[1])
		ref = colL[3]
		alt = colL[4]
		formatL = colL[8].split(':')
		t_infoL = colL[tcol].split(':')
		n_infoL = colL[ncol].split(':')

		t_MQS = t_infoL[formatL.index('MQS')]
		t_SC = (map(lambda x: int(x), t_infoL[formatL.index('SC')].split(',')))
		t_AD = t_infoL[formatL.index('AD')]
		t_AD_A = int(t_AD.split(',')[1])
		t_DP = int(t_infoL[formatL.index('DP')])
		n_DP = int(n_infoL[formatL.index('DP')])
		t_FS_PVAL = fisher.pvalue(t_SC[0],t_SC[1], t_SC[2],t_SC[3]).two_tail
		t_FS_PVAL=-10 * math.log10(t_FS_PVAL)
		t_REnd = t_infoL[formatL.index('REnd')]
		t_RSta = t_infoL[formatL.index('RStart')]

		reasonL = []
		if 'SOMATIC' not in colL[7]:
			reasonL += ['germline_event']
		if float(t_MQS.split(',')[0]) < TH_MAPQ or float(t_MQS.split(',')[1]) < TH_MAPQ_A:
			reasonL += ['poor_mapq']
		if t_FS_PVAL > TH_FS_PVAL or (0 in t_SC):
			reasonL += ['strand_bias']
		if float(t_AD_A)/t_DP < TH_TFRAC:
			reasonL += ['low_allele_frac']
		if t_DP < TH_DP or t_AD_A < TH_AD_A:
			reasonL += ['low_coverage']
		if n_DP < TH_DP:
			reasonL += ['low_coverage_in_normal']
		if (chr,pos,ref,alt) in repeatH:
			reasonL += ['repeated_sequence']
		if (TAG_KGP in colL[7]) or (TAG_ESP in colL[7]):
			reasonL += ['found_in_normal_panel']
		if (float(t_REnd.split(',')[0]) <= TH_POS_MED and float(t_REnd.split(',')[1]) <= TH_POS_MAD) or (float(t_RSta.split(',')[0]) <= TH_POS_MED and float(t_RSta.split(',')[1]) <= TH_POS_MAD):
			reasonL += ['clustered_position']

		if reasonL == []:
			info = colL[7]
			if info == '.':
				info = 'T_FS_PVAL=%s' % t_FS_PVAL
			else:
				info = '%s;T_FS_PVAL=%s' % (info, t_FS_PVAL)
			selectedFile.write('%s\t%s\t%s\n' % ('\t'.join(colL[:7]), info, '\t'.join(colL[8:])))
			outFile.write('%s\t%s\t%s\t%s\t%s\t%s\tKEEP\n' % (chr,pos,ref,alt, '\t'.join(colL[8:]), t_FS_PVAL))
		else:
			reasonS = ','.join(reasonL)
			outFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (chr,pos,ref,alt, '\t'.join(colL[8:]), t_FS_PVAL, reasonS))
	#for line
	selectedFile.flush()
	selectedFile.close()
	outFile.flush()
	outFile.close()


def filter_indel_single(inFileN, selectedFileN, outFileN, TH_FS_PVAL=0.1, TH_MAPQ=50, TH_MAPQ_A=30, TH_DP=10, TH_AD_A=5, TH_TFRAC=0.01, TH_POS_MED=10, TH_POS_MAD=3):
	repeatH = find_overlap_repeat(inFileN)
	inFile = open(inFileN)
	selectedFile = open(selectedFileN, 'w')
	outFile = open(outFileN, 'w')
	for line in inFile:
		if line[0] == '#':
			selectedFile.write(line)
			if line[2:12].lower() == 'fileformat':
				selectedFile.write('##INFO=<ID=FS_PVAL,Number=1,Type=Float,Description="Phred-scale p-value from Fisher\'s exact test of strand-bias">\n')
				selectedFile.flush()
			continue
		colL = line.rstrip().split('\t')
		chr = colL[0]
		pos = int(colL[1])
		ref = colL[3]
		alt = colL[4]
		formatL = colL[8].split(':')
		infoL = colL[9].split(':')

		MQS = infoL[formatL.index('MQS')]
		SC = (map(lambda x: int(x), infoL[formatL.index('SC')].split(',')))
		AD = infoL[formatL.index('AD')]
		AD_A = int(AD.split(',')[1])
		DP = int(infoL[formatL.index('DP')])
		FS_PVAL=fisher.pvalue(SC[0],SC[1], SC[2],SC[3]).two_tail
		FS_PVAL=-10 * math.log10(FS_PVAL)
		REnd = infoL[formatL.index('REnd')]
		RSta = infoL[formatL.index('RStart')]

		reasonL = []
		if float(MQS.split(',')[0]) < TH_MAPQ or float(MQS.split(',')[1]) < TH_MAPQ_A:
			reasonL += ['poor_mapq']
		if FS_PVAL > TH_FS_PVAL or (0 in SC):
			reasonL += ['strand_bias']
		if float(AD_A)/DP < TH_TFRAC:
			reasonL += ['low_allele_frac']
		if DP < TH_DP or AD_A < TH_AD_A:
			reasonL += ['low_coverage']
		if (chr,pos,ref,alt) in repeatH:
			reasonL += ['repeated_sequence']
		if (TAG_KGP in colL[7]) or (TAG_ESP in colL[7]):
			reasonL += ['found_in_normal_panel']
		if (float(REnd.split(',')[0]) <= TH_POS_MED and float(REnd.split(',')[1]) <= TH_POS_MAD) or (float(RSta.split(',')[0]) <= TH_POS_MED and float(REnd.split(',')[1]) <= TH_POS_MAD):
			reasonL += ['clustered_position']

		if reasonL == []:
			info = colL[7]
			if info == '.':
				info = 'FS_PVAL=%s' % FS_PVAL
			else:
				info = '%s;FS_PVAL=%s' % (info, FS_PVAL)
			selectedFile.write('%s\t%s\t%s\n' % ('\t'.join(colL[:7]), info, '\t'.join(colL[8:])))
			outFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\tKEEP\n' % (chr,pos,ref,alt, colL[8], colL[9], FS_PVAL))
		else:
			reasonS = ','.join(reasonL)
			outFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (chr,pos,ref,alt, colL[8], colL[9], FS_PVAL, reasonS))
		#if
	#line
	outFile.flush()
	outFile.close()
	selectedFile.flush()
	selectedFile.close()

if __name__ == '__main__':
#	filter_indel_single('IRCR_GBM14_446_T_CS.indels_known.vcf', 'IRCR_GBM14_446_T_CS.indels_filtered.vcf', 'IRCR_GBM14_446_T_CS.indels_filtered.out')
#	filter_indel_single('IRCR_GBM14_416_T_CS.indels_known.vcf', 'IRCR_GBM14_416_T_CS.indels_filtered.vcf', 'IRCR_GBM14_416_T_CS.indels_filtered.out')
#	for PREFIX in ['IRCR_GBM14_482','IRCR_LC14_278','IRCR_GBM14_485','IRCR_GBM14_488','IRCR_MBT14_166','IRCR_MBT14_167']:
#		inFN='%s.indels_known.vcf' % PREFIX
#		selN='%s.indels_filtered.vcf' % PREFIX
#		outN='%s.indels_filtered.out' % PREFIX
#		filter_indel_single(inFN, selN, outN)
#	filter_indel_single('/EQL5/pipeline/CS_mut/CS11_14_00796_T_CS/CS11_14_00796_T_CS.indels_annot.vcf', 'haha.vcf','haha.out')
	filter_indel_paired('/EQL3/pipeline/somatic_mutation/IRCR_GBM14_529_T_SS/IRCR_GBM14_529_T_SS.indels_pair.vcf','haha.vcf','haha.out',TH_FS_PVAL=200,TH_MAPQ=50,TH_MAPQ_A=25,TH_DP=10,TH_AD_A=2,TH_TFRAC=0.01,TH_POS_MED=10,TH_POS_MAD=3)
