#!/usr/bin/python

import sys, os
import mymysql
from mybasic import rc
from mybasic import compl

#contig	position	context	ref_allele	alt_allele	tumor_name	normal_name	score	dbsnp_site	covered	power	tumor_power	normal_power	total_pairs	improper_pairs	map_Q0_reads	t_lod_fstar	tumor_f	contaminant_fraction	contaminant_lod	t_ref_count	t_alt_count	t_ref_sum	t_alt_sum	t_ref_max_mapq	t_alt_max_mapq	t_ins_count	t_del_count	normal_best_gt	init_n_lod	n_ref_count	n_alt_count	n_ref_sum	n_alt_sum	judgement
def mutation_signature(inDir, outName=''):
	if outName == '':
		outFile = sys.stdout
	else:
		outFile = open(outName, 'w')

	outFile.write("samp_id\tmutation\tcontext\tfreq\tn_mut\tn_total\n")
	mutFileNL = map(lambda x: x.rstrip(), os.popen('ls %s/*.mutect | grep -v union_pos' % inDir).readlines())
	for mutFileN in mutFileNL:
		sampN = mutFileN.split('/')[-1].split('.')[0].split('_')[0]
		print sampN, mutFileN
		mutFile = open(mutFileN, 'r')
		mutFile.readline()
		headerL = mutFile.readline().rstrip().split('\t')
		idxH = {}
		sigH = {}
		cntH = {}
		for i in range(len(headerL)):
			idxH[headerL[i]] = i
		total = 0
		for line in mutFile:
			colL = line.rstrip().split('\t')
			chr = colL[idxH['contig']]
			pos = colL[idxH['position']]
			context = colL[idxH['context']]
			ref = colL[idxH['ref_allele']]
			alt = colL[idxH['alt_allele']]
			status = colL[idxH['judgement']]
			if status == 'REJECT' or chr == 'chrMT' or chr == 'chrM':
				continue

			total += 1
			tri = context[2] + ref + context[4]
			if ref == 'C' or ref == 'T':
				nt_ch = ref + '>' + alt
			else:
				nt_ch = rc(ref) + '>' + rc(alt)
				tri = rc(tri)
			if (nt_ch,tri) in sigH:
				sigH[(nt_ch,tri)] += 1
			else:
				sigH[(nt_ch,tri)] = 1
			if (nt_ch) in cntH:
				cntH[(nt_ch)] += 1
			else:
				cntH[(nt_ch)] = 1

		mutFile.close()
		for key in sigH:
			(type, tri) = key
			freq = sigH[key]
			outFile.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (sampN, type, tri, freq, cntH[type], total))
	outFile.flush()
	outFile.close()

if __name__ == '__main__':
	mutation_signature('/EQL3/pipeline/somatic_mutect', '/EQL1/NSL/WXS/results/mutation/mutation_signature_mutect_20140227.txt')
#	mutation_signature('/EQL3/pipeline/somatic_mutect', '')
