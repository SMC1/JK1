#!/usr/bin/python

import sys
import os

seqGroupName = ['hsa_mature','hsa_hp','seedLib','castellii_supcon','ath_cDNA','hsa_ORF_noAS','cerevisiae_ORF','mmu_miRNA_SJ','castellii_ORF','cerevisiae_rRNA','ath_miRNA','mmu_miRNA','dme_miRNA','castellii','shRNA_pilot_templ'] 
	#, 'pombe', 'tair9', 'dm3', 'shRNA1', 'hsa_miRNA']
seqName = [['hsa_mir'],['hsa_hp'],['array_55k_seq_final'], ['Scastellii_040406_super-contigs'],['ath_cDNA_20090619'],['hsa_ORF_noAS'],['orf_coding'], ['mmu_hp_mt'], ['Scastellii_040406_orfs'], ['cerevisiae_rRNA'], ['ath_hp'],['mmu_hp'], \
	['dme_hp'],['contig570'],['array_6.5k_seq_final']]
	#[['chr1','chr2','chr3'], ['chr1','chr2','chr3','chr4','chr5','chrC','chrM'], 
	#['chr'+s for s in ['2L','2LHet','2R','2RHet','3L','3LHet','3R','3RHet','4','X','XHet','YHet','U','Uextra','M']],
	#['hairpin_filtered'], ['hsa_hp']]

for i in [0,1]: #range(len(seqGroupName)):

	temp = []

	for seqN in seqName[i]:

		temp.append('./%s/%s.fa' % (seqGroupName[i],seqN))

	os.system('~/bin/bowtie-0.10.0/bowtie-build %s ./indexes/%s' % (','.join(temp),seqGroupName[i]))
