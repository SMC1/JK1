#!/usr/bin/python

import os, sys
import myvep

cosmic='/data1/Sequence/cosmic/hg19_cosmic_v54_120711.vcf'
dbsnp='/data1/Sequence/ucsc_hg19/annot/dbsnp_135.hg19.sort.vcf'
REF='/data1/Sequence/ucsc_hg19/hg19.fasta'

headerL = ['contig', 'position', 'context', 'ref_allele', 'alt_allele', 'tumor_name', 'normal_name', 'score', 'dbsnp_site', 'covered', 'power', 'tumor_power', 'normal_power', 'total_pairs', 'improper_pairs', 'map_Q0_reads', 't_lod_fstar', 'tumor_f', 'contaminant_fraction', 'contaminant_lod', 't_ref_count', 't_alt_count', 't_ref_sum', 't_alt_sum', 't_ref_max_mapq', 't_alt_max_mapq', 't_ins_count', 't_del_count', 'normal_best_gt', 'init_n_lod', 'n_ref_count', 'n_alt_count', 'n_ref_sum', 'n_alt_sum', 'judgement']
idxH = {}
for i in range(len(headerL)):
	idxH[headerL[i]] = i

def get_mutect_read_counts_s(inFileName):
	inFile = open(inFileName,'r')
	inFile.readline() ##ver
	inFile.readline() ##header
	
	outH = {}
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

def get_mutect_read_counts(primName, recurName):
	## output: (chr,pos,ref,alt): (P_alt,P_ref,R_alt,R_ref,N_alt,N_ref)
	cntH = {}

	## prim first
	primH = get_mutect_read_counts_s(primName)
	recurH = get_mutect_read_counts_s(recurName)

	for key in primH:
		(P_alt,P_ref,N_alt,N_ref,P_stat) = primH[key]
		cntH[key] = {'P_alt':P_alt, 'P_ref':P_ref, 'N_alt':N_alt, 'N_ref':N_ref, 'P_stat':P_stat}
	for key in recurH:
		(R_alt,R_ref,N_alt,N_ref,R_stat) = recurH[key]
		if cntH[key]['P_stat'] == 'REJECT' and R_stat == 'REJECT': ## delete this
			del cntH[key]
		else: ##both must coincide
			cntH[key]['R_alt'] = R_alt
			cntH[key]['R_ref'] = R_ref
			cntH[key]['R_stat'] = R_stat
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
DirL = ['/EQL1/NSL/WXS/exome_20130529/','/EQL1/NSL/exome_bam/','/EQL1/pipeline/ExomeSeq_20130723/']

trioH = {}
for line in trioF:
	cols = line.rstrip().split('\t')
	tid = cols[0]
	role = cols[1]
	sid = cols[2]
	prefix = cols[3]

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
		trioH[tid] = {}
		if role == 'Primary':
			trioH[tid]['prim_id'] = sid
		elif role == 'Recurrent':
			trioH[tid]['recur_id'] = sid
		trioH[tid][role] = {}
		if len(mutFileNL) > 0:
			trioH[tid][role]['mut'] = mutFileNL[0].rstrip()
		if len(sampFileNL) > 0:
			trioH[tid][role]['bam'] = sampFileNL[0].rstrip()
		if len(vepFileNL) > 0:
			trioH[tid][role]['vep'] = vepFileNL[0].rstrip()
	else:
		if role == 'Primary':
			trioH[tid]['prim_id'] = sid
		elif role == 'Recurrent':
			trioH[tid]['recur_id'] = sid
		trioH[tid][role] = {}
		if len(mutFileNL) > 0:
			trioH[tid][role]['mut'] = mutFileNL[0].rstrip()
		if len(sampFileNL) > 0:
			trioH[tid][role]['bam'] = sampFileNL[0].rstrip()
		if len(vepFileNL) > 0:
			trioH[tid][role]['vep'] = vepFileNL[0].rstrip()

totalVar = {}
annotH = {}
for tid in trioH:
	pair = 'S%s-S%s' % (trioH[tid]['prim_id'], trioH[tid]['recur_id'])
	outPosFile = '/EQL1/PrimRecur/paired/somatic/%sT_%sT.union.intervals' % (trioH[tid]['prim_id'], trioH[tid]['recur_id'])
#	if os.path.isfile(outPosFile):
#		os.system('rm -f %s' % outPosFile)
	## 1. union of somatic sites
#	os.system('(grep -v REJECT %s | grep "^chr"| cut -f %s,%s; grep -v REJECT %s | grep "^chr" | cut -f %s,%s) | sort -k1d,1 -k2n,2 | uniq > tmp' % (trioH[tid]['Primary']['mut'], idxH['contig']+1,idxH['position']+1, trioH[tid]['Recurrent']['mut'], idxH['contig']+1,idxH['position']+1))
#	for i in range(1, 23):
#		os.system('grep -w "chr%s" tmp | sort -k2n,2 | awk \'{print $1":"$2"-"$2}\' >> %s' % (i, outPosFile))
#	for i in ['X','Y','M']:
#		os.system('grep -w "chr%s" tmp | sort -k2n,2 | awk \'{print $1":"$2"-"$2}\' >> %s' % (i, outPosFile))
#	os.system('rm tmp')
	## 2. run mutect on collected sites
	outPrim = '/EQL1/PrimRecur/paired/somatic/%sT.union_pos.mutect' % (trioH[tid]['prim_id'])
	outRecur = '/EQL1/PrimRecur/paired/somatic/%sT.union_pos.mutect' % (trioH[tid]['recur_id'])
#	os.system('''java -jar /home/tools/muTect/muTect.jar --analysis_type MuTect --force_output --force_alleles --reference_sequence %s --cosmic %s --dbsnp %s\
#		--input_file:normal %s --input_file:tumor %s --out %s --intervals %s''' % (REF, cosmic, dbsnp, trioH[tid]['Normal']['bam'], trioH[tid]['Primary']['bam'], outPrim, outPosFile))
#	os.system('''java -jar /home/tools/muTect/muTect.jar --analysis_type MuTect --force_output --force_alleles --reference_sequence %s --cosmic %s --dbsnp %s\
#		--input_file:normal %s --input_file:tumor %s --out %s --intervals %s''' % (REF, cosmic, dbsnp, trioH[tid]['Normal']['bam'], trioH[tid]['Recurrent']['bam'], outRecur, outPosFile))
	## 3. output merge mutect + vep
	union = get_mutect_read_counts(outPrim, outRecur)
	annot = myvep.parse_vep(trioH[tid]['Primary']['vep'])
	for key in annot:
		if key not in annotH:
			annotH[key] = annot[key]
	annot = myvep.parse_vep(trioH[tid]['Recurrent']['vep'])
	for key in annot:
		if key not in annotH:
			annotH[key] = annot[key]
	totalVar[pair] = union

##header
outFile = open('/EQL1/PrimRecur/paired/somatic/8pair_mutect_union.dat', 'w')
outFile.write('dType\tsId_pair\tlocus\tref\talt\tp_status\tr_status\tp_mt\tp_wt\tr_mt\tr_wt\tn_mt\tn_wt\tGID\tTID\t%s\n' % '\t'.join(myvep.outField))
for pair in totalVar:
	cur = totalVar[pair]
	for var in cur:
		(chr,pos,ref,alt) = var
		chr2 = chr[3:]
		if chr2 == 'M':
			chr2 = 'MT'
		if (chr2,pos,ref,alt) not in annotH:
			sys.stderr.write(','.join(var))
			continue
		annot = annotH[(chr2,pos,ref,alt)]
		cnt = cur[var]
		for gene in annot:
			outFile.write('mutation_normal\t%s' % pair)
			outFile.write('\t%s:%s~%s%s>%s\t%s\t%s' % (chr,pos,pos,ref,alt,ref,alt))
			outFile.write('\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (cnt['P_stat'],cnt['R_stat'],cnt['P_alt'],cnt['P_ref'],cnt['R_alt'],cnt['R_ref'],cnt['N_alt'],cnt['N_ref']))
			outFile.write('\t%s' % gene)
			if len(annot[gene]['tid']) > 0:
				outFile.write('\t%s' % ','.join(annot[gene]['tid'].values()))
			else:
				outFile.write('\t')
			for col in myvep.outField:
				if col in annot[gene]:
					outFile.write('\t%s' % ','.join(annot[gene][col]))
				else:
					outFile.write('\t')
			outFile.write('\n')
outFile.flush()
outFile.close()
