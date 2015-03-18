#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mysetting
from glob import glob

COLUMNS = "contig,position,context,ref_allele,alt_allele,tumor_name,normal_name,score,dbsnp_site,covered,power,tumor_power,normal_power,normal_power_nsp,normal_power_wsp,total_pairs,improper_pairs,map_Q0_reads,init_t_lod,t_lod_fstar,t_lod_lqs,t_lod_fstar_forward,t_lod_fstar_reverse,tumor_f,tumor_f_lb,contaminant_fraction,contaminant_lod,t_q20_count,t_ref_count,t_alt_count,t_ref_sum,t_alt_sum,t_ref_max_mapq,t_alt_max_mapq,t_ins_count,t_del_count,normal_best_gt,init_n_lod,n_lod_fstar,normal_f,normal_f_quals,normal_artifact_lod_tf,normal_artifact_lod_low_tf,normal_artifact_lod_nf,normal_artifact_lod_nfq,n_q20_count,n_ref_count,n_alt_count,n_ref_sum,n_alt_sum,power_to_detect_positive_strand_artifact,power_to_detect_negative_strand_artifact,strand_bias_counts,tumor_alt_fpir_median,tumor_alt_fpir_mad,tumor_alt_rpir_median,tumor_alt_rpir_mad,alt_fpir,alt_rpir,powered_filters,normal_artifact_power_tf,normal_artifact_power_low_tf,normal_artifact_power_nf,normal_global_qll,normal_local_qll,normal_qmodel_lod,observed_in_normals_count,failure_reasons,judgement"
DEPTH_TH = 5000
HD_GAP_FRAC_TH = 0.001

def mutect_pair(inDirN, outDirN, genome='hg19', server='smc1', pbs=False):
	mutect_pair_with_interval(inDirN=inDirN, outDirN=outDirN, useInterval=False, genome=genome, server=server, pbs=pbs)

def mutect_pair_with_interval(inDirN, outDirN, useInterval=False, genome='hg19', server='smc1', pbs=False):
	tBamNL = filter(lambda x: re.match('(.*)\.recal\.bam$', x) and '_B_' not in x and '-B.recal' not in x, os.listdir(inDirN))
	nBamN = filter(lambda x: re.match('(.*)\.recal\.bam$', x) and ('_B_' in x or '-B.recal' in x), os.listdir(inDirN))[0]

	ref = mysetting.ucscRefH[server][genome]
	cosmic = mysetting.cosmicH[server][genome]
	dbsnp = mysetting.dbsnpH[server][genome]
	kgp = mysetting.all_1kgH[server][genome]
	esp = mysetting.espH[server][genome]

	for tBamN in tBamNL:
		sampN = re.search('(.*).recal.bam', os.path.basename(tBamN)).group(1)
		cmd = 'java -Xmx8g -jar /home/tools/muTect/muTect.jar --analysis_type MuTect --tumor_f_pretest 0.005 --min_qscore 15 -dcov 50000 --fraction_contamination 0.005 --enable_extended_output'

		if useInterval:
			intervalN = glob('%s/*point*.intervals' % outDirN)[0]
			out = '%s/%s.union_pos.mutect' % (outDirN,sampN)
			vcf_out = '%s/%s.union_pos.mutect.vcf' % (outDirN,sampN)
			log = '%s/%s.union_pos.mutect_pair.log' % (outDirN,sampN)
			vcf_flt = '%s/%s.union_pos.mutect_filter.vcf' % (outDirN,sampN)
			cmd = '%s --intervals %s --force_output --reference_sequence %s --cosmic %s --dbsnp %s --input_file:normal %s/%s --input_file:tumor %s/%s --out %s --vcf %s > %s' % (cmd, intervalN, ref, cosmic, dbsnp, inDirN,nBamN, inDirN,tBamN, out, vcf_out, log)
			if not os.path.isfile(out):
				print cmd
				os.system(cmd)
			if not os.path.isfile(vcf_flt):
				print  vcf_flt
				refine_output(vcf_out, out, vcf_flt)
		else:
			out = '%s/%s.mutect' % (outDirN,sampN)
			vcf_out = '%s/%s.mutect_pair.vcf' % (outDirN,sampN)
			log = '%s/%s.mutect_pair.log' % (outDirN,sampN)
			vcf_flt = '%s/%s.mutect_pair_filter.vcf' % (outDirN,sampN)
			cmd = '%s --reference_sequence %s --cosmic %s --dbsnp %s --input_file:normal %s/%s --input_file:tumor %s/%s --out %s --vcf %s > %s' % (cmd, ref, cosmic, dbsnp, inDirN,nBamN, inDirN,tBamN, out, vcf_out, log)
			if not os.path.isfile(out):
				print cmd
				os.system(cmd)
			if not os.path.isfile(vcf_flt):
				print vcf_flt
				refine_output(vcf_out, out, vcf_flt)

## reprocess wes samples with previous mutect run (without --enable_enable_extended_output)
def rerun_wrapper(dirN):
	mutect_pair_rerun(inDirN=dirN, outDirN=dirN)

def mutect_pair_rerun(inDirN, outDirN, genome='hg19', server='smc1', pbs=False):
	old_dir='/EQL3/pipeline/somatic_mutect'
	sampN = os.path.basename(inDirN)
	prev_run = '%s/%s.mutect' % (old_dir, sampN)
	if os.path.isfile(prev_run):
		print sampN
		##make interval from previous run
		tBamN = filter(lambda x: re.match('(.*)\.recal\.bam$', x) and '_B_' not in x, os.listdir(inDirN))[0]
		nBamN = filter(lambda x: re.match('(.*)\.recal\.bam$', x) and '_B_' in x, os.listdir(inDirN))[0]

		ref = mysetting.ucscRefH[server][genome]
		cosmic = mysetting.cosmicH[server][genome]
		dbsnp = mysetting.dbsnpH[server][genome]
		kgp = mysetting.all_1kgH[server][genome]
		esp = mysetting.espH[server][genome]

		interval_out = outDirN + '/' + sampN + '.prev_mutect_run.intervals'
		cmd = '''awk 'OFS="\\t" {if (NR>2) {print $1":"$2"-"$2}}' %s > %s''' % (prev_run, interval_out)
		os.system(cmd)
		out = '%s/%s.mutect_rerun' % (outDirN,sampN)
		vcf_out = '%s/%s.mutect_rerun.vcf' % (outDirN,sampN)
		log = '%s/%s.mutect_pair_rerun.log' % (outDirN,sampN)
		vcf_flt = '%s/%s.mutect_rerun_filter.vcf' % (outDirN,sampN)
		cmd = 'java -Xmx8g -jar /home/tools/muTect/muTect.jar --analysis_type MuTect --tumor_f_pretest 0.005 --min_qscore 15 -dcov 50000 --fraction_contamination 0.005 --enable_extended_output'
		cmd = '%s --reference_sequence %s --cosmic %s --dbsnp %s --input_file:normal %s/%s --input_file:tumor %s/%s --out %s --vcf %s --intervals %s> %s' % (cmd, ref,cosmic,dbsnp, inDirN,nBamN, inDirN,tBamN, out,vcf_out, interval_out, log)
		if not os.path.isfile(out):
			print cmd
			os.system(cmd)
		if not os.path.isfile(vcf_flt):
			refine_output(vcf_out, out, vcf_flt)

def mutect_STD(inDirName, genome='hg19', server='smc1', pbs=False):
	
	inputFileNL = filter(lambda x: re.match('(.*)\.recal\.bam$', x), os.listdir(inDirName))

	print 'Files: %s' % inputFileNL, len(inputFileNL)

	sampNL = list(set([re.match('(.*)\.recal\.bam$',inputFileN).group(1) for inputFileN in inputFileNL]))
	sampNL.sort()

	print 'samples: %s' % sampNL

	ref = mysetting.ucscRefH[server][genome]
	
	cmd = 'java -Xmx8g -jar /home/tools/muTect/muTect.jar --analysis_type MuTect --artifact_detection_mode -dcov 50000 --fraction_contamination 0.005 --tumor_f_pretest 0.005 --min_qscore 15 --reference_sequence %s --enable_extended_output' % ref

	for sampN in sampNL:

		print sampN

		ibam = '%s/%s.recal.bam' % (inDirName, sampN)
		out = '%s/%s.mutect' % (mysetting.ctrMutectDir, sampN)
		vcf = '%s/%s.mutect.vcf' % (mysetting.ctrMutectDir, sampN)
		log = '%s/%s.mutect_std.log' % (mysetting.ctrMutectDir, sampN)
		vcf_flt = '%s/%s.mutect_filter.vcf' % (mysetting.ctrMutectDir, sampN)
		if not os.path.isfile(out):
			cmd = '%s --input_file:tumor %s -vcf %s --out %s > %s' % (cmd, ibam, vcf, out, log)
			print cmd
			os.system(cmd)
		if not os.path.isfile(vcf_flt):
			refine_output(vcf, out, vcf_flt)

def refine_output(vcfFileN, mutFileN, outFileN):
	## add strand count & rescue candidates rejected only by gap event
	vcfFile = open(vcfFileN)
	mutFile = open(mutFileN)
	outFile = open(outFileN, 'w')

	headerL = COLUMNS.split(',')
	mutH = {}
	for line in mutFile:
		if line[0] == '#':
			continue
		if line[:6] == 'contig':
			headerL = line.rstrip().split('\t')
			continue

		colL = line.rstrip().split('\t')

		chr = colL[headerL.index('contig')]
		pos = colL[headerL.index('position')]
		ref = colL[headerL.index('ref_allele')]
		alt = colL[headerL.index('alt_allele')]
		depth = int(colL[headerL.index('t_ref_count')]) + int(colL[headerL.index('t_alt_count')])
		n_gap_event = int(colL[headerL.index('t_ins_count')]) + int(colL[headerL.index('t_del_count')])
		if depth < 1:
			continue
		gap_event_frac = float(n_gap_event)/depth
		strand_cnt = re.match('\((.*)\)', colL[headerL.index('strand_bias_counts')]).group(1)
		fail = colL[headerL.index('failure_reasons')]
		call = colL[headerL.index('judgement')]

		if call != 'REJECT' or (depth > DEPTH_TH and gap_event_frac <= HD_GAP_FRAC_TH and fail == 'nearby_gap_events'):
			mutH[(chr,pos,ref,alt)] = strand_cnt
	#for
	mutFile.close()

	idx_t = 9
	idx_n = 10
	for line in vcfFile:
		if line[0] == '#':
			if line[:6] == '#CHROM':
				colL = line.rstrip().split('\t')
				if '_B_' in colL[9] or colL[9] == 'none':
					idx_t = 10
					idx_n = 9
			if line[:6] == '##INFO':
				outFile.write('##FORMAT=<ID=SC,Number=4,Type=Integer,Description="Strandedness: counts of forward-/reverse-aligned reference and mut-surpporting reads (FwdRef,RevRef,FwdAlt,RefAlt)">\n')
			outFile.write(line)
			continue
		#if

		colL = line.rstrip().split('\t')
		chr = colL[0]
		pos = colL[1]
		ref = colL[3]
		alt = colL[4]
		if (chr,pos,ref,alt) in mutH: ##selected
			if colL[6] == 'REJECT':
				colL[6] = 'RESCUED'
			outFile.write('%s' % '\t'.join(colL[:8]))
			outFile.write('\t%s:SC' % colL[8])
			if idx_t == 9:
				outFile.write('\t%s:%s' % (colL[9], mutH[(chr,pos,ref,alt)]))
			else:
				outFile.write('\t%s:0,0,0,0' % colL[9])
			if len(colL) > 10:
				if idx_t == 10:
					outFile.write('\t%s:%s' % (colL[10], mutH[(chr,pos,ref,alt)]))
				else:
					outFile.write('\t%s:0,0,0,0' % colL[10])
			outFile.write('\n')
		#if
	#for
	outFile.flush()
	outFile.close()

def mutect_PON_wrapper(argS):
	(dir, genome, server, pbs) = argS
	print argS
	mutect_PON(dir, genome, server, pbs)

def mutect_PON(inDirName, genome='hg19', server='smc1', pbs=False):
	
	inputFileNL = filter(lambda x: re.match('(.*)\.recal\.bam$', x), os.listdir(inDirName))

	print 'Files: %s' % inputFileNL, len(inputFileNL)

	sampNL = list(set([re.match('(.*)\.recal\.bam$',inputFileN).group(1) for inputFileN in inputFileNL]))
	sampNL.sort()

	print 'samples: %s' % sampNL

	ref = mysetting.ucscRefH[server][genome]
	cosmic = mysetting.cosmicH[server][genome]
	dbsnp = mysetting.dbsnpH[server][genome]
	kgp = mysetting.all_1kgH[server][genome]
	esp = mysetting.espH[server][genome]

	cmd = 'java -Xmx8g -jar /home/tools/muTect/muTect.jar --analysis_type MuTect --tumor_f_pretest 0.005 -dcov 50000 --fraction_contamination 0.005 --min_qscore 15 --enable_extended_output'
	cmd = '%s --reference_sequence %s --cosmic %s --dbsnp %s --normal_panel %s --normal_panel %s' % (cmd, ref, cosmic, dbsnp, kgp, esp)

	for sampN in sampNL:
		
		print sampN

		ibam = '%s/%s.recal.bam' % (inDirName, sampN)
		out = '%s/%s.mutect' % (inDirName, sampN)
		vcf = '%s/%s.mutect_single.vcf' % (inDirName, sampN)
		log = '%s/%s.mutect_single.log' % (inDirName, sampN)
		vcf_flt = '%s/%s.mutect_single_filter.vcf' % (inDirName, sampN)
		if not os.path.isfile(vcf):
			cmd = '%s --input_file:tumor %s -vcf %s --out %s > %s' % (cmd, ibam, vcf, out, log)
			print cmd
			os.system(cmd)
		if not os.path.isfile(vcf_flt):
			refine_output(vcf, out, vcf_flt)

if __name__ == '__main__':
#	mutect_PON('/EQL5/pipeline/CS_mut/IRCR_GBM14_459_T01_CS')
#	for dir in glob('/EQL5/pipeline/CS_mut/*CS'):
#		mutect_PON(dir)
#	refine_output('/EQL5/pipeline/CS_mut/IRCR_GBM14_459_T01_CS/IRCR_GBM14_459_T01_CS_mutect.vcf','/EQL5/pipeline/CS_mut/IRCR_GBM14_459_T01_CS/IRCR_GBM14_459_T01_CS.mutect','haha')

#	from multiprocessing import Pool
#	dirL = glob('/EQL3/pipeline/somatic_mutation/*S')
#	pool = Pool(processes = 8)
#	pool.map(rerun_wrapper, dirL)
#	mutect_pair('/EQL3/pipeline/somatic_mutation/IRCR_GBM14_567_T_SS','/EQL3/pipeline/somatic_mutation/IRCR_GBM14_567_T_SS')

	## for all exome
#	mutect_pair('/EQL5/pipeline/CS_mut/IRCR_GBM14_460_T_CS/IRCR_GBM14_460_T_CS.recal.bam','/EQL5/pipeline/CS_mut/IRCR_GBM14_460_B_CS/IRCR_GBM14_460_B_CS.recal.bam','.')
#	mutect_PON('/EQL3/pipeline/SGI20140331_xsq2mut/S316_T_SS')
#	for dir in mysetting.wxsBamDirL[:-1] + mysetting.oldPipelineL:
#		dirL = filter(lambda x: '_B_' in x and os.path.isdir('%s/%s' % (dir, x)), os.listdir(dir))
#		if len(dirL) > 0:
#			for d in dirL:
#				if 'S4C' in d or 'S6C' in d:
#					continue
#				print dir, d
#	mutect_STD('/EQL3/pipeline/SGI20140331_xsq2mut/S316_B_SS')
#	for dir in filter(lambda x: os.path.isdir('/EQL6/pipeline/CS_HAPMAP20/'+x), os.listdir('/EQL6/pipeline/CS_HAPMAP20')):
#		mutect_STD('/EQL6/pipeline/CS_HAPMAP20/'+dir, genome='hg19', server='smc1', pbs=False)

#test
#	mutect_PON('/EQL7/pipeline/SGI20140930_xsq2mut/IRCR_GBM14_567_T_SS/', genome='hg19', server='smc1', pbs=False)
	from multiprocessing import Pool
	argL = []
	for sid in ['554','562']:
		dir=glob('/EQL7/pipeline/*xsq2mut/*%s_T*_SS/' % sid)[0]
		print dir
		argS = (dir, 'hg19', 'smc1',False)
		argL.append(argS)
	pool = Pool(processes = 2)
	pool.map(mutect_PON_wrapper, argL)
#	from multiprocessing import Pool
#	argL = []
#	for sid in ['S223','S240','S243','S323']:
#		argS = ('/EQL7/pipeline/SGI20131216_xsq2mut/%s_T_SS/' % sid, 'hg19', 'smc1', False)
#		argL.append(argS)
#	pool = Pool(processes = 4)
#	pool.map(mutect_PON_wrapper, argL)
