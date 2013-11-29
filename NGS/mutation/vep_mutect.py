#!/usr/bin/python

import sys, os, time
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

	vep_in = '%s/%s.mutect_vep_in' % (outDirName, sampN)
	vep_out = '%s/%s.mutect_vep_out.vcf' % (outDirName, sampN)
	outName = '%s/%s.mutect_vep.dat' % (outDirName, sampN)
	
	vepInFile = open(vep_in, 'w')
	varSize = 0
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

		if status == 'REJECT':
			continue
		
		varSize += 1
		if len(ref) == len(alt):
			if len(ref) == 1: # point mutation
				vepInFile.write('%s\t%s\t%s\t%s/%s\t+\n' % (chr, pos, pos, ref, alt))
			else:
				ref = ref[1:]
				alt = alt[1:]
				start = pos + 1
				end = start + len(alt) - 1
				vepInFile.write('%s\t%s\t%s\t%s/%s\t+\n' % (chr, start, end, ref, alt))
		elif len(ref) < len(alt): # insertion
			alt = alt[len(ref):]
			pos = pos + len(ref)
			ref = '-'
			start = pos + 1
			end = pos
			vepInFile.write('%s\t%s\t%s\t%s/%s\t+\n' % (chr, start, end, ref, alt))
		elif len(ref) > len(alt): # deletion
			ref = ref[len(alt):]
			pos = pos + len(alt)
			alt = '-'
			start = pos
			end = pos + len(ref) - 1
			vepInFile.write('%s\t%s\t%s\t%s/%s\t+\n' % (chr, start, end, ref, alt))
	inFile.close()
	vepInFile.flush()
	vepInFile.close()
	os.system('perl /home/tools/VEP/variant_effect_predictor.pl --no_progress --fork 5 --config /home/tools/VEP/vep_config -i %s --format ensembl -o %s --vcf --no_stats > %s/%s.mutect_vep.log 2>&1' % (vep_in, vep_out, outDirName,sampN))
	vepH = myvep.parse_vep(vep_out)
	myvep.print_vep(vepH, outName)

if __name__ == '__main__':
	vep_mutect('/EQL1/NSL/exome_bam/mutation/S025_T_TS.mutect', '/EQL1/NSL/exome_bam/mutation')
