#!/usr/bin/python

import sys, os, re
import mysetting
from glob import glob
import filter_indel

TH_FS_PVAL_H = {'CS': 120, 'SS': 200} ## threshold for phred-scale p-value by Fisher test for strand bias
TH_MAPQ = 50 ## threshold for mapping quality around indel (ref)
TH_MAPQ_A = 25 ## threshold for mapping quality around indel (alt)
TH_TFRAC = 0.01 ## threshold for allele fraction
TH_POS_MED = 10 ## threshold for median of indel read position
TH_POS_MAD = 3 ## threshold for MAD of indel read position
COV_H = {'CS':50, 'SS':10}
CNT_H = {'CS':10, 'SS':4}

def single_mode(inDirN, outDirN, pl='CS', genome='hg19', server='smc1', pbs=False):
	inFileNL = filter(lambda x: re.match('(.*)\.recal\.bam$', x), os.listdir(inDirN))

	sampNL = list(set([re.match('(.*)\.recal\.bam$', inputFileN).group(1) for inputFileN in inFileNL]))

#	print sampNL

	ref = mysetting.ucscRefH[server][genome]
	dbsnp = mysetting.dbsnpH[server][genome]
	kgpf = mysetting.all_1kgH[server][genome]
	espf = mysetting.espH[server][genome]
	cosmic = mysetting.cosmicH[server][genome]

	cov = '-filter \'COV<%s\' -filter \'CONS_CNT<%s\'' % (COV_H[pl], CNT_H[pl])
	opt = '-filter \'INDEL_F<0.01\' %s -filter \'INDEL_CF<0.7\' -dcov 50000 --maxNumberOfReads 50000 --min_mapping_quality_score 15' % cov
	flt = '-rf DuplicateRead --filter_mismatching_base_and_quals -rf BadMate -rf UnmappedRead -rf NotPrimaryAlignment -rf MappingQualityUnavailable -rf MappingQuality'


	#if not pbs
	for sampN in sampNL:
		cmd = 'java -Xmx8g -jar /home/tools/GATK-2.2/GenomeAnalysisTK.jar -T SomaticIndelDetector --unpaired -R %s %s %s' % (ref, opt, flt)
#		print sampN
		ibam = '%s/%s.recal.bam' % (inDirN, sampN)
		out = '%s/%s.indels_single.out' % (outDirN, sampN)
		vcf = '%s/%s.indels_single.vcf' % (outDirN, sampN)
		log = '%s/%s.somaticindeldetector_single.log' %  (outDirN, sampN)

		cmd = '%s --input_file:tumor %s -o %s --verboseOutput %s > %s' % (cmd, ibam, vcf, out, log)
		print cmd
		os.system(cmd)

		intvl = '%s/%s.indels_single.intervals' % (outDirN, sampN)
		cmd = 'awk \'OFS="\\t" {print $1":"$2-5"-"$3+5}\' %s > %s' % (out, intvl)
		print cmd
		os.system(cmd)

		annot_cmd = 'java -Xmx8g -jar /home/tools/GATK/GenomeAnalysisTK.jar -T VariantAnnotator -R %s --dbsnp %s --comp:KGPF %s --comp:ESPF %s -dcov 50000' % (ref, dbsnp, kgpf, espf)
		annot_vcf = '%s/%s.indels_single_annot.vcf' % (outDirN, sampN)
		annot_cmd = '%s -I %s --variant %s -o %s -L %s >> %s' % (annot_cmd, ibam, vcf, annot_vcf, intvl, log)
		print annot_cmd
		os.system(annot_cmd)

		flt_vcf = '%s/%s.indels_single_filter.vcf' % (outDirN, sampN)
		flt_out = '%s/%s.indels_single_filter.out' % (outDirN, sampN)
		filter_indel.filter_indel_single(annot_vcf, flt_vcf, flt_out, TH_FS_PVAL_H[pl], TH_MAPQ, TH_MAPQ_A, COV_H[pl], CNT_H[pl], TH_TFRAC, TH_POS_MED, TH_POS_MAD)

		os.system('cut -f 1 %s | uniq >> %s' % (flt_out, log))

def paired_mode(inDirN, outDirN, pl='CS', genome='hg19', server='smc1', pbs=False):
	paired_mode_with_interval(inDirN=inDirN, outDirN=outDirN, pl=pl, useInterval=False, genome=genome, server=server, pbs=pbs)

def paired_mode_with_interval(inDirN, outDirN, pl='CS', useInterval=False, genome='hg19', server='smc1', pbs=False):
	tbamL = filter(lambda x: re.match('(.*)\.recal\.bam$', x) and '_B_' not in x and '-B.recal' not in x, os.listdir(inDirN))
	nbam = filter(lambda x: re.match('(.*)\.recal\.bam$', x) and ('_B_' in x or '-B.recal' in x), os.listdir(inDirN))[0]

	ref = mysetting.ucscRefH[server][genome]
	dbsnp = mysetting.dbsnpH[server][genome]
	kgpf = mysetting.all_1kgH[server][genome]
	espf = mysetting.espH[server][genome]
	cosmic = mysetting.cosmicH[server][genome]

	cov = '-filter \'T_COV<%s\' -filter \'N_COV<%s\' -filter \'T_CONS_CNT<%s\'' % (COV_H[pl], COV_H[pl], CNT_H[pl])
	opt = '-filter \'T_INDEL_F<0.01\' %s -filter \'T_INDEL_CF<0.7\' -dcov 50000 --maxNumberOfReads 50000 --min_mapping_quality_score 15' % cov
	flt = '-rf DuplicateRead --filter_mismatching_base_and_quals -rf BadMate -rf UnmappedRead -rf NotPrimaryAlignment -rf MappingQualityUnavailable -rf MappingQuality'

	for tbam in tbamL:
		cmd = 'java -Xmx8g -jar /home/tools/GATK-2.2/GenomeAnalysisTK.jar -T SomaticIndelDetector -R %s %s %s' % (ref, opt, flt)
		sampN = re.search('(.*)\.recal\.bam$', os.path.basename(tbam)).group(1)

		if useInterval:
			intvalN = glob('%s/*indel*union*intervals' % inDirN)[0]
			prefix = '.union_pos'
			cmd = '%s -L %s' % (cmd, intvalN)
		else:
			prefix = ''

		out = '%s/%s%s.indels_pair.out' % (outDirN,sampN,prefix)
		vcf = '%s/%s%s.indels_pair.vcf' % (outDirN,sampN,prefix)
		log = '%s/%s%s.somaticindeldetector_pair.log' % (outDirN,sampN,prefix)

		cmd = '%s --input_file:normal %s/%s --input_file:tumor %s/%s -o %s --verboseOutput %s > %s' % (cmd, inDirN,nbam, inDirN,tbam, vcf, out, log)

		print cmd
		os.system(cmd)

		intvl = '%s/%s%s.indels_pair.intervals' % (outDirN,sampN,prefix)
		cmd = 'awk \'OFS="\\t" {print $1":"$2-5"-"$3+5}\' %s > %s' % (out, intvl)
		print cmd
		os.system(cmd)

		annot_cmd = 'java -Xmx8g -jar /home/tools/GATK/GenomeAnalysisTK.jar -T VariantAnnotator -R %s --dbsnp %s --comp:KGPF %s --comp:ESPF %s -dcov 50000' % (ref, dbsnp, kgpf, espf)
		annot_vcf = '%s/%s%s.indels_pair_annot.vcf' % (outDirN,sampN,prefix)
		annot_cmd = '%s -I %s/%s --variant %s -o %s -L %s >> %s' % (annot_cmd, inDirN,tbam, vcf, annot_vcf, intvl, log)
		print annot_cmd
		os.system(annot_cmd)

		flt_vcf = '%s/%s%s.indels_pair_filter.vcf' % (outDirN,sampN,prefix)
		flt_out = '%s/%s%s.indels_pair_filter.out' % (outDirN,sampN,prefix)
		filter_indel.filter_indel_paired(annot_vcf, flt_vcf, flt_out, TH_FS_PVAL_H[pl], TH_MAPQ, TH_MAPQ_A, COV_H[pl], CNT_H[pl], TH_TFRAC, TH_POS_MED, TH_POS_MAD)
	#for tbam
	os.system('cut -f 1 %s | uniq >> %s' % (flt_out, log))

#	out = '%s/%s.indels_pair.out' % (outDirN, sampN)
#	vcf = '%s/%s.indels_pair.vcf' % (outDirN, sampN)
#	log = '%s/%s.somaticindeldetector_pair.log' % (outDirN, sampN)
#
#	cmd = 'java -Xmx8g -jar /home/tools/GATK-2.2/GenomeAnalysisTK.jar -T SomaticIndelDetector -R %s %s %s' % (ref, opt, flt)
#	cmd = '%s --input_file:normal %s/%s --input_file:tumor %s/%s -o %s --verboseOutput %s > %s' % (cmd, inDirN,nbam, inDirN,tbam, vcf,out, log)
#	print cmd
#	os.system(cmd)
#
#	intvl = '%s/%s.indels_pair.intervals' % (outDirN, sampN)
#	cmd = 'awk \'OFS="\\t" {print $1":"$2-5"-"$3+5}\' %s > %s' % (out, intvl)
#	print cmd
#	os.system(cmd)
#
#	annot_cmd = 'java -Xmx8g -jar /home/tools/GATK/GenomeAnalysisTK.jar -T VariantAnnotator -R %s --dbsnp %s --comp:KGPF %s --comp:ESPF %s -dcov 50000' % (ref, dbsnp, kgpf, espf)
#	annot_vcf = '%s/%s.indels_pair_annot.vcf' % (outDirN, sampN)
#	annot_cmd = '%s -I %s/%s --variant %s -o %s -L %s >> %s' % (annot_cmd, inDirN,tbam, vcf, annot_vcf, intvl, log)
#	print annot_cmd
#	os.system(annot_cmd)
#	
#	flt_vcf = '%s/%s.indels_pair_filter.vcf' % (outDirN, sampN)
#	flt_out = '%s/%s.indels_pair_filter.out' % (outDirN, sampN)
#	filter_indel.filter_indel_paired(annot_vcf, flt_vcf, flt_out, TH_FS_PVAL_H[pl], TH_MAPQ, TH_MAPQ_A, COV_H[pl], CNT_H[pl], TH_TFRAC, TH_POS_MED, TH_POS_MAD)

def paired_wrapper(argS):
	(tbam, nbam, dirN, sampN, pl) = argS
	paired_mode(tbam, nbam, dirN, sampN, pl)

if __name__ == '__main__':
	## test run
#	single_mode('/EQL5/pipeline/CS_mut/IRCR_MBT14_172_T_CS', '/home/ihlee')
#	import mybasic
#	mybasic.add_module_path(['NGS/mutation'])
#	import vep_batch
#	vep_batch.run_vep('/home/ihlee/IRCR_GBM14_459_T02_CS.indels_filter.vcf','IRCR_GBM14_459_T02_CS', '/home/ihlee', 'REJECT', fork=True)

#	paired_mode('/EQL5/pipeline/CS_mut/IRCR_GBM14_504_T03_CS/IRCR_GBM14_504_T03_CS.recal.bam','/EQL5/pipeline/CS_mut/IRCR_GBM14_504_B_CS/IRCR_GBM14_504_B_CS.recal.bam', '.', 'IRCR_GBM14_504_T_CS')
#	single_mode('/EQL5/pipeline/CS_mut/IRCR_GBM14_416_T_CS', '/home/ihlee/haha')

	##batch for cancerscan
#	dirL = filter(lambda x: os.path.isdir('/EQL5/pipeline/CS_mut/' + x), os.listdir('/EQL5/pipeline/CS_mut'))
#	for dir in dirL:
#		baseDir = '/EQL5/pipeline/CS_mut/%s' % dir
#		print baseDir
#		single_mode(baseDir, baseDir)

	#batch single mode run for exome
#	from multiprocessing import Pool
##	for dir in mysetting.wxsBamDirL[:-1]+mysetting.oldPipelineL + ['/EQL1/NSL/exome_bam/bam_link']:
#		if 'somatic_mutect' in dir:
#			continue
#		single_mode(dir,'/EQL4/pipeline/indel_batch','SS')
#		for d in filter(lambda x: os.path.isdir(dir+'/'+x), os.listdir(dir)):
#			single_mode(dir+'/'+d,'/EQL4/pipeline/indel_batch','SS')
#	pool = Pool(processes = 10)
#	pool.map(paired_wrapper, argL)

	for dir in glob('/EQL7/pipeline/*xsq2mut/*S'):
		if '_B_' in dir or 'PC_' in dir:
			continue
		print dir
#		mutect_PON(inDirName=dir, genome='hg19', server='smc1', pbs=False)
		single_mode(dir, dir, 'SS')
		sys.exit(1)
