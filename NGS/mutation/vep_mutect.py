#!/usr/bin/python

import sys, os, time, re
import myvep

#['contig', 'position', 'context', 'ref_allele', 'alt_allele', 'tumor_name', 'normal_name', 'score', 'dbsnp_site', 'covered', 'power', 'tumor_power', 'normal_power', 'total_pairs', 'improper_pairs', 'map_Q0_reads', 't_lod_fstar', 'tumor_f', 'contaminant_fraction', 'contaminant_lod', 't_ref_count', 't_alt_count', 't_ref_sum', 't_alt_sum', 't_ref_max_mapq', 't_alt_max_mapq', 't_ins_count', 't_del_count', 'normal_best_gt', 'init_n_lod', 'n_ref_count', 'n_alt_count', 'n_ref_sum', 'n_alt_sum', 'judgement']

def vep_mutect(inFileName, outDirName):
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
	
#	vepInFile = open(vep_in, 'w')
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
#				vepInFile.write('%s\t%s\t%s\t%s/%s\t+\n' % (chr, pos, pos, ref, alt))
			else:
				ref = ref[1:]
				alt = alt[1:]
				start = pos + 1
				end = start + len(alt) - 1
				varH[(chr,pos,ref,alt)] = (t_ref,t_alt,n_ref,n_alt)
#				vepInFile.write('%s\t%s\t%s\t%s/%s\t+\n' % (chr, start, end, ref, alt))
		elif len(ref) < len(alt): # insertion
			alt = alt[len(ref):]
			pos = pos + len(ref)
			ref = '-'
			start = pos + 1
			end = pos
			varH[(chr,pos,ref,alt)] = (t_ref,t_alt,n_ref,n_alt)
#			vepInFile.write('%s\t%s\t%s\t%s/%s\t+\n' % (chr, start, end, ref, alt))
		elif len(ref) > len(alt): # deletion
			ref = ref[len(alt):]
			pos = pos + len(alt)
			alt = '-'
			start = pos
			end = pos + len(ref) - 1
			varH[(chr,pos,ref,alt)] = (t_ref,t_alt,n_ref,n_alt)
#			vepInFile.write('%s\t%s\t%s\t%s/%s\t+\n' % (chr, start, end, ref, alt))
		#if
	#for line
	inFile.close()
#	vepInFile.flush()
#	vepInFile.close()
#	os.system('perl /home/tools/VEP/variant_effect_predictor.pl --no_progress --fork 7 --config /home/tools/VEP/vep_config -i %s --format ensembl -o %s --vcf --no_stats > %s/%s.mutect_vep.log 2>&1' % (vep_in, vep_out, outDirName,sampN))
	vepH = myvep.parse_vep(vep_out)
	myvep.print_vep(vepH, outFileN=outName, cntH=varH, sampN=sampN)
#	outFile = open(outName, 'w')
#	for (chr,pos,ref,alt) in vepH:
#		cur = vepH[(chr, pos, ref, alt)]
#		chr_tmp = chr
#		if chr == 'M':
#			chr_tmp = 'MT'
#		(t_ref,t_alt,n_ref,n_alt) = varH[(chr_tmp,int(pos),ref,alt)]
#		for gene in cur:
#			if (len(cur[gene]['strand']) != 1):
#				print cur[gene]['strand']
#				sys.exit(1)
#			outFile.write('%s\tchr%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (sampN, chr, pos, pos, ref, alt, n_ref, n_alt, t_ref, t_alt, ','.join(cur[gene]['strand']), gene, ','.join(cur[gene]['ch_dna']), ','.join(cur[gene]['ch_aa']), ','.join(cur[gene]['ch_type'])))
#	outFile.flush()
#	outFile.close()

if __name__ == '__main__':
#	vep_mutect('/EQL1/NSL/exome_bam/mutation/S025_T_TS.mutect', '/EQL1/NSL/exome_bam/mutation')
	vep_mutect('/EQL3/pipeline/somatic_mutect/S012_T_SS.mutect', '/EQL3/pipeline/somatic_mutect')
