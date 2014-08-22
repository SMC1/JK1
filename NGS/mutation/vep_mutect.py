#!/usr/bin/python

import sys, os, time, re
import myvep
import myvep_old

#['contig', 'position', 'context', 'ref_allele', 'alt_allele', 'tumor_name', 'normal_name', 'score', 'dbsnp_site', 'covered', 'power', 'tumor_power', 'normal_power', 'total_pairs', 'improper_pairs', 'map_Q0_reads', 't_lod_fstar', 'tumor_f', 'contaminant_fraction', 'contaminant_lod', 't_ref_count', 't_alt_count', 't_ref_sum', 't_alt_sum', 't_ref_max_mapq', 't_alt_max_mapq', 't_ins_count', 't_del_count', 'normal_best_gt', 'init_n_lod', 'n_ref_count', 'n_alt_count', 'n_ref_sum', 'n_alt_sum', 'judgement']

def vep_mutect_new(inFileN, sampN, outDirName, fork=False):
	fName = os.path.basename(inFileN).replace('.vcf','')
	vep_in = '%s/%s_vep_in' % (outDirName, fName)
	os.system("sed -e 's/^chrM/MT/' -e 's/^chr//' %s > %s" % (inFileN, vep_in))
	vep_out = '%s/%s_vep.vcf' % (outDirName, fName)
	outName = '%s/%s_vep.dat' % (outDirName, fName)
	log = '%s/%s_vep.log' % (outDirName, fName)

	if fork:
		doFork='--fork 10'
	else:
		doFork=''
	os.system('perl /home/tools/VEP/variant_effect_predictor.pl --no_progress %s --config /home/tools/VEP/vep_config -i %s --format vcf -o %s --vcf --no_stats > %s 2>&1' % (doFork, vep_in, vep_out, log))
	myvep.process_cancerscan_vep(vep_out, sampN, outName)
	

def vep_mutect_old(inFileName, outDirName):
	inFile = open(inFileName,'r')
	ver = inFile.readline().rstrip()
	headerL = inFile.readline().rstrip().split('\t')
	idxH = {}
	for i in range(len(headerL)):
		idxH[headerL[i]] = i

	sampN = inFileName.split('/')[-1].split('.')[0]

	vep_in = '%s/%s.mutect_vep_in' % (outDirName, sampN) ## select only somatic mutations
	vep_out = '%s/%s.mutect_vep_out.vcf' % (outDirName, sampN) ## keep full annotation in vcf
	outName = '%s/%s.mutect_vep.dat' % (outDirName, sampN) ## gene_sym, ch_dna (HGVSc), ch_aa (HGVSp), ch_type (): Substitution - Missense, etc...
	
	vepInFile = open(vep_in, 'w')
	varSize = 0
	varH = {}
	for line in inFile:
		colL = line.rstrip().split('\t')

		chr = colL[idxH['contig']]
		if chr == 'chrM' or chr == 'chrMT':
			chr = 'MT'
		else:
			chr = chr[3:]
		pos = int(colL[idxH['position']])
		ref = colL[idxH['ref_allele']]
		alt = colL[idxH['alt_allele']]
		status = colL[idxH['judgement']]
		t_ref = colL[idxH['t_ref_count']]
		t_alt = colL[idxH['t_alt_count']]
		n_ref = colL[idxH['n_ref_count']]
		n_alt = colL[idxH['n_alt_count']]

		if status == 'REJECT':
			continue
	
		varSize += 1
		if len(ref) == len(alt):
			if len(ref) == 1: # point mutation
				varH[(chr,pos,ref,alt)] = (t_ref,t_alt,n_ref,n_alt)
				vepInFile.write('%s\t%s\t%s\t%s/%s\t+\n' % (chr, pos, pos, ref, alt))
			else:
				ref = ref[1:]
				alt = alt[1:]
				start = pos + 1
				end = start + len(alt) - 1
				varH[(chr,pos,ref,alt)] = (t_ref,t_alt,n_ref,n_alt)
				vepInFile.write('%s\t%s\t%s\t%s/%s\t+\n' % (chr, start, end, ref, alt))
		elif len(ref) < len(alt): # insertion
			alt = alt[len(ref):]
			pos = pos + len(ref)
			ref = '-'
			start = pos + 1
			end = pos
			varH[(chr,pos,ref,alt)] = (t_ref,t_alt,n_ref,n_alt)
			vepInFile.write('%s\t%s\t%s\t%s/%s\t+\n' % (chr, start, end, ref, alt))
		elif len(ref) > len(alt): # deletion
			ref = ref[len(alt):]
			pos = pos + len(alt)
			alt = '-'
			start = pos
			end = pos + len(ref) - 1
			varH[(chr,pos,ref,alt)] = (t_ref,t_alt,n_ref,n_alt)
			vepInFile.write('%s\t%s\t%s\t%s/%s\t+\n' % (chr, start, end, ref, alt))
		#if
	#for line
	inFile.close()
	vepInFile.flush()
	vepInFile.close()
	os.system('perl /home/tools/VEP/variant_effect_predictor.pl --no_progress --fork 7 --config /home/tools/VEP/vep_config -i %s --format ensembl -o %s --vcf --no_stats > %s/%s.mutect_vep.log 2>&1' % (vep_in, vep_out, outDirName,sampN))
	vepH = myvep_old.parse_vep(vep_out)
	if outName == '':
		outFile = sys.stdout
	else:
		outFile = open(outName, 'w')
	for (chr,pos,ref,alt) in vepH:
		cur = vepH[(chr, pos, ref, alt)]
		chr_tmp = chr
		if chr == 'M':
			chr_tmp = 'MT'
		(t_ref,t_alt,n_ref,n_alt) = varH[(chr_tmp,int(pos),ref,alt)]
		infoH = myvep_old.print_vep_item(cur)
		for gene in infoH:
			outFile.write('%s\tchr%s\t%s\t%s\t%s\t%s' % (sampN, chr, pos, pos, ref, alt))
			outFile.write('\t%s\t%s\t%s\t%s' % (n_ref, n_alt, t_ref, t_alt))
			if gene == '-':
				out_gene = ''
			else:
				out_gene = gene
			outFile.write('\t%s\t%s\t%s\t%s\t%s\n' % (infoH[gene]['strand'], out_gene, infoH[gene]['ch_dna'], infoH[gene]['ch_aa'], infoH[gene]['ch_type']))
	outFile.flush()
	outFile.close()

if __name__ == '__main__':
	vep_mutect_old('/EQL3/pipeline/somatic_mutect/IRCR_GBM14_499_T02_SS.mutect', '.')
#	vep_mutect('/EQL1/NSL/exome_bam/mutation/S025_T_TS.mutect', '/EQL1/NSL/exome_bam/mutation')
#	vep_mutect('/EQL3/pipeline/somatic_mutect/S14A_T_SS.mutect', '/EQL3/pipeline/somatic_mutect')
#	vep_mutect('/EQL6/pipeline/CR_150_xsq2mut/CR11_T_150_P.mutect','/EQL6/pipeline/CR_150_xsq2mut')
#	kep_mutect('/EQL6/pipeline/CR_150_xsq2mut/CR11_T_150_M.mutect','/EQL6/pipeline/CR_150_xsq2mut')
#	vep_mutect_new('/EQL1/pipeline/CS20140618_xsq2mut/IRCR_GBM12_143_T_CS/IRCR_GBM12_143_T_CS_mutect.vcf', 'IRCR_GBM12_143_T_CS', '/EQL1/pipeline/CS20140618_xsq2mut/IRCR_GBM12_143_T_CS')
