#!/usr/bin/python

import sys, os, weblogolib
import mybasic

def mutect_weblogo(sampN, inFileN, outFileN):
	inFile = open(inFileN, 'r')
	inFile.readline() #comment line
	headerL = inFile.readline().rstrip().split('\t')
	idxH = {}
	for i in range(len(headerL)):
		idxH[headerL[i]] = i

	tmpFile = open('tmp','w')
	for line in inFile:
		colL = line.rstrip().split('\t')
		context = colL[idxH['context']]
		ref = colL[idxH['ref_allele']]
		alt = colL[idxH['alt_allele']]
		status = colL[idxH['judgement']]
		if status == 'REJECT':
			continue

		head = context[:3]
		tail = context[-3:]
		context = head + ref + tail
		if ref not in ['C','T']:
			context = mybasic.rc(context)
			ref = mybasic.rc(ref)
			alt = mybasic.rc(alt)

		if ref == 'C' and alt == 'T':## TMZ context only
			tmpFile.write('%s\n' % context)
	tmpFile.flush()
	tmpFile.close()
	
	fin = open('tmp','r')
	seqs = weblogolib.read_seq_data(fin)
	data = weblogolib.LogoData.from_seqs(seqs)
	options = weblogolib.LogoOptions()
	options.show_fineprint = False
	options.first_index = -3
	options.logo_title = sampN
	format = weblogolib.LogoFormat(data, options)
	fout = open(outFileN, 'w')
	weblogolib.pdf_formatter(data, format, fout)
	os.system('mv tmp  %s.weblogo.input' % sampN)

if __name__ == '__main__':
	mutect_weblogo('S302','/EQL3/pipeline/somatic_mutect/S302_T_SS.mutect','S302.weblogo.pdf')
	mutect_weblogo('S171','/EQL3/pipeline/somatic_mutect/S171_T_SS.mutect','S171.weblogo.pdf')
	mutect_weblogo('S585','/EQL3/pipeline/somatic_mutect/S585_T_SS.mutect','S585.weblogo.pdf')

#	contig	position	context	ref_allele	alt_allele	tumor_name	normal_name	score	dbsnp_sitecovered	power	tumor_power	normal_power	total_pairs	improper_pairs	map_Q0_reads	t_lod_fstar	tumor_f	contaminant_fraction	contaminant_lod	t_ref_count	t_alt_count	t_ref_sum	t_alt_sum	t_ref_max_mapq	t_alt_max_mapq	t_ins_count	t_del_count	normal_best_gt	init_n_lod	n_ref_count	n_alt_count	n_ref_sum	n_alt_sum	judgement
