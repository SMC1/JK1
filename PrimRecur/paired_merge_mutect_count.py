#!/usr/bin/python

import os, sys
import myvep

MINQ = 15 # minimum base quality score
MIN_T_FRAC = 0.01 ## minimum allele fraction in tumor
MAX_N_READ = 5   ## maximum mut. read counts in matched-normal
MAX_N_FRAC = 0.05 ## maximum allele fraction in matched-normal

cosmic='/data1/Sequence/cosmic/hg19_cosmic_v54_120711.vcf'
dbsnp='/data1/Sequence/ucsc_hg19/annot/dbsnp_135.hg19.sort.vcf'
REF='/data1/Sequence/ucsc_hg19/hg19.fasta'

MUTECT_CMD = 'java -jar /home/tools/muTect/muTect.jar --analysis_type MuTect --reference_sequence %s --cosmic %s --dbsnp %s -dt NONE --tumor_f_pretest %s --min_qscore %s --max_alt_alleles_in_normal_count %s --max_alt_allele_in_normal_fraction %s --force_alleles --force_output' % (REF, cosmic, dbsnp, MIN_T_FRAC, MINQ, MAX_N_READ, MAX_N_FRAC)

headerL = ['contig', 'position', 'context', 'ref_allele', 'alt_allele', 'tumor_name', 'normal_name', 'score', 'dbsnp_site', 'covered', 'power', 'tumor_power', 'normal_power', 'total_pairs', 'improper_pairs', 'map_Q0_reads', 't_lod_fstar', 'tumor_f', 'contaminant_fraction', 'contaminant_lod', 't_ref_count', 't_alt_count', 't_ref_sum', 't_alt_sum', 't_ref_max_mapq', 't_alt_max_mapq', 't_ins_count', 't_del_count', 'normal_best_gt', 'init_n_lod', 'n_ref_count', 'n_alt_count', 'n_ref_sum', 'n_alt_sum', 'judgement']

idxH = {}

for i in range(len(headerL)):
	idxH[headerL[i]] = i

def get_mutect_read_counts_s(inFileNameL):
	outH = {}
	for inFileName in inFileNameL:
		if inFileName == '':
			continue
		inFile = open(inFileName,'r')
		inFile.readline() ##ver
		inFile.readline() ##header
	
		for line in inFile:
			colL = line.rstrip().split('\t')

			chr = colL[idxH['contig']]
			pos = colL[idxH['position']]
			ref = colL[idxH['ref_allele']]
			alt = colL[idxH['alt_allele']]
			T_ref = colL[idxH['t_ref_count']]
			T_alt = colL[idxH['t_alt_count']]
			N_ref = colL[idxH['n_ref_count']]
			N_alt = colL[idxH['n_alt_count']]
			status = colL[idxH['judgement']]
			outH[(chr,pos,ref,alt)] = (T_alt,T_ref,N_alt,N_ref,status)
		inFile.close()
	return outH

def get_mutect_read_counts(primName, recurName, primName2='', recurName2=''):
	## output: (chr,pos,ref,alt): (P_alt,P_ref,R_alt,R_ref,N_alt,N_ref)
	cntH = {}

	## prim first
	primH = get_mutect_read_counts_s([primName])
	recurH = get_mutect_read_counts_s([recurName])

	for key in primH:
		(P_alt,P_ref,N_alt,N_ref,P_stat) = primH[key]
		if P_stat != 'REJECT':
			t_frac = int(P_alt) / (int(P_alt)+int(P_ref))
			n_frac = int(N_alt) / (int(N_alt)+int(N_ref))
#			if int(N_alt) > MAX_N_READ or t_frac < MIN_T_FRAC or n_frac > MAX_N_FRAC:
#				P_stat = 'REJECT'
		cntH[key] = {'P_alt':P_alt, 'P_ref':P_ref, 'N_alt':N_alt, 'N_ref':N_ref, 'P_stat':P_stat}
	for key in recurH:
		(R_alt,R_ref,N_alt,N_ref,R_stat) = recurH[key]
		if R_stat != 'REJECT':
			t_frac = int(R_alt) / (int(R_alt)+int(R_ref))
			n_frac = int(N_alt) / (int(N_alt)+int(N_ref))
#			if int(N_alt) > MAX_N_READ or t_frac < MIN_T_FRAC or n_frac > MAX_N_FRAC:
#				R_stat = 'REJECT'
		if key not in cntH:
			print primName
			print recurName
			print primName2
			print recurName2
			print key
			sys.exit(1)
		if cntH[key]['P_stat'] == 'REJECT' and R_stat == 'REJECT': ## delete this
			del cntH[key]
		else: ##both must coincide
			cntH[key]['R_alt'] = R_alt
			cntH[key]['R_ref'] = R_ref
			cntH[key]['R_stat'] = R_stat
#	all_pos = cntH.keys()
#	for key in all_pos:
#		if len(cntH[key]) < 8:
#			del cntH[key]
	return cntH

def add_annot(primName, recurName, dbH):
	inFile = open(primName, 'r')
	for line in inFile:
		colL = line.rstrip().split('\t')
		key = tuple(colL[:4])
		gid = colL[4]
		annot = (colL[5:])
		if key in dbH:
			if gid not in dbH[key]:
				dbH[key][gid] = annot
		else:
			dbH[key] = {}
			dbH[key][gid] = annot
	inFile.close()

	inFile = open(recurName, 'r')
	for line in inFile:
		colL = line.rstrip().split('\t')
		key = tuple(colL[:4])
		gid = colL[4]
		annot = (colL[5:])
		if key in dbH:
			if gid not in dbH[key]:
				dbH[key][gid] = annot
		else:
			dbH[key] = {}
			dbH[key][gid] = annot
	inFile.close()

trioF = open('mutect_trio_info.txt', 'r')
#DirL = ['/EQL1/NSL/WXS/exome_20130529/','/EQL1/NSL/exome_bam/','/EQL1/pipeline/ExomeSeq_20130723/']
DirL = ['/EQL3/pipeline/somatic_mutect/']

trioH = {}
for line in trioF:
	if line[0] == '#':
		continue
	cols = line.rstrip().split('\t')
	tid = cols[0]
	role = cols[1]
	sid = cols[2]
	if len(cols) > 3:
		prefix = cols[3]
	else:
		if role == 'Normal':
			prefix = 'S' + sid + '_B_SS'
		else:
			prefix = 'S' + sid + '_T_SS'

	sampFileNL = []
	for dir in DirL:
		sampFileNL += os.popen('find %s -name %s*recal.bam' % (dir, prefix)).readlines()
		sampFileNL += os.popen('find %s -name *%s' % (dir, prefix)).readlines()

	mutFileNL = []
	for dir in DirL:
		mutFileNL += os.popen('find %s -name %s*mutect' % (dir, prefix)).readlines()
	
	vepFileNL = []
	for dir in DirL:
		vepFileNL += os.popen('find %s -name %s*mutect_vep_out.vcf' % (dir, prefix)).readlines()
	
	if tid not in trioH:
		trioH[tid] = {'norm_id':[], 'prim_id':[], 'recur_id':[], 'Normal':{'mut':{}, 'bam':{}, 'vep':{}}, 'Primary':{'mut':{}, 'bam':{}, 'vep':{}}, 'Recurrent':{'mut':{}, 'bam':{}, 'vep':{}}}

	if role == 'Primary':
		trioH[tid]['prim_id'].append(sid)
	elif role == 'Recurrent':
		trioH[tid]['recur_id'].append(sid)
	elif role == 'Normal':
		trioH[tid]['norm_id'].append(sid)

	if len(mutFileNL) > 0:
		trioH[tid][role]['mut'][sid] = mutFileNL[0].rstrip()
	if len(sampFileNL) > 0:
		trioH[tid][role]['bam'][sid] = sampFileNL[0].rstrip()
	if len(vepFileNL) > 0:
		trioH[tid][role]['vep'][sid] = vepFileNL[0].rstrip()

OutDir = '/EQL3/pipeline/somatic_mutect'
run = (False, False, True) # 1, 2, 3
sys.stdout.write('dType\tsId_pair\tlocus\tref\talt\tSYMBOL\tch_dna\tch_aa\tp_status\tr_status\tp_mt\tp_wt\tr_mt\tr_wt\tn_mt\tn_wt\teffect\n')
for tid in trioH:
	#skip samples without recurrent
	if len(trioH[tid]['Recurrent']['vep']) < 1:
		continue

	norm_id = trioH[tid]['norm_id'][0]
	prim_id = trioH[tid]['prim_id'][0]
	if run[0]:
		files = ' '.join(trioH[tid]['Primary']['mut'].values()) + ' ' + ' '.join(trioH[tid]['Recurrent']['mut'].values())
		for recur_id in trioH[tid]['recur_id']:
			outPosFile = '%s/%sT_%sT.union.intervals' % (OutDir, prim_id, recur_id)
			## 1. union of somatic sites
			if os.path.isfile(outPosFile):
				os.system('rm -f %s' % outPosFile)
			cmd = 'cat %s | grep -v REJECT | grep -v "^chrM" | grep "^chr" | cut -f %s,%s | sort -k1d,1 -k2n,2 | uniq > tmp' % (files, idxH['contig']+1, idxH['position']+1)
			os.system(cmd)
			for i in range(1, 23):
				cmd = 'grep -w "^chr%s" tmp | sort -k2n,2 | awk \'{print $1":"$2"-"$2}\' >> %s' % (i, outPosFile)
				os.system(cmd)
			for i in ['X','Y']:
				cmd = 'grep -w "^chr%s" tmp | sort -k2n,2 | awk \'{print $1":"$2"-"$2}\' >> %s' % (i, outPosFile)
				os.system(cmd)
			os.system('rm -f tmp')
	#if run[0]

	for recur_id in trioH[tid]['recur_id']:
		annotH = {}
		outPosFile = '%s/%sT_%sT.union.intervals' % (OutDir, prim_id, recur_id)
		pair = 'S%s-S%s' % (prim_id, recur_id)

		outPrim = '%s/%sT.union_pos.mutect' % (OutDir, prim_id)
		outRecur = '%s/%sT.union_pos.mutect' % (OutDir, recur_id)
		if run[1]:
			## 2. run mutect on union sites for pair
			cmd = '%s --input_file:normal %s --input_file:tumor %s --out %s --intervals %s' % (MUTECT_CMD, trioH[tid]['Normal']['bam'][norm_id], trioH[tid]['Primary']['bam'][prim_id], outPrim, outPosFile)
			os.system(cmd)
			cmd = '%s --input_file:normal %s --input_file:tumor %s --out %s --intervals %s' % (MUTECT_CMD, trioH[tid]['Normal']['bam'][norm_id], trioH[tid]['Recurrent']['bam'][recur_id], outRecur, outPosFile)
			os.system(cmd)
		#if run[1]

		if run[2]:
			## 3. output merge mutect + vep
			union = get_mutect_read_counts(outPrim, outRecur)
			annot = myvep.parse_vep(trioH[tid]['Primary']['vep'][prim_id])
			for key in annot:
				if key not in annotH:
					annotH[key] = annot[key]
			annot = myvep.parse_vep(trioH[tid]['Recurrent']['vep'][recur_id])
			for key in annot:
				if key not in annotH:
					annotH[key] = annot[key]

			for var in union:
				(chr,pos,ref,alt) = var
				chr2 = chr[3:]
				if chr2 == 'M':
					chr2 = 'MT'
				cnt = union[var]
				if (chr2,pos,ref,alt) in annotH:
					annot = annotH[(chr2,pos,ref,alt)]
					for gene in annot:
						sys.stdout.write('mutect_somatic\t%s' % pair)
						sys.stdout.write('\t%s:%s~%s%s>%s\t%s\t%s\t%s' % (chr, pos, pos, ref, alt, ref, alt, gene))
						if 'ch_dna' in annot[gene]:
							sys.stdout.write('\t%s' % ','.join(annot[gene]['ch_dna']))
						else:
							sys.stdout.write('\t-')
						if 'ch_aa' in annot[gene]:
							sys.stdout.write('\t%s' % ','.join(annot[gene]['ch_aa']))
						else:
							sys.stdout.write('\t-')
						sys.stdout.write('\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (cnt['P_stat'],cnt['R_stat'],cnt['P_alt'],cnt['P_ref'],cnt['R_alt'],cnt['R_ref'],cnt['N_alt'],cnt['N_ref']))
						if 'ch_type' in annot[gene]:
							sys.stdout.write('\t%s' % ','.join(annot[gene]['ch_type']))
						else:
							sys.stdout.write('\t-')
						sys.stdout.write('\n')
				else:
						sys.stdout.write('mutect_somatic\t%s' % pair)
						sys.stdout.write('\t%s:%s~%s%s>%s\t%s\t%s\t-\t-\t-' % (chr, pos, pos, ref, alt, ref, alt))
						sys.stdout.write('\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (cnt['P_stat'],cnt['R_stat'],cnt['P_alt'],cnt['P_ref'],cnt['R_alt'],cnt['R_ref'],cnt['N_alt'],cnt['N_ref']))
						sys.stdout.write('\t-\n')
		#if run[2]
