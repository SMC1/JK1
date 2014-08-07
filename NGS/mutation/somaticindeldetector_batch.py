#!/usr/bin/python

import sys, os, re
import mysetting
from glob import glob
import filter_indel

COV_H = {'CS':50, 'SS':10}
CNT_H = {'CS':10, 'SS':2}

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
		cmd = 'java -jar /home/tools/GATK-2.2/GenomeAnalysisTK.jar -T SomaticIndelDetector --unpaired -R %s %s %s' % (ref, opt, flt)
#		print sampN
		ibam = '%s/%s.recal.bam' % (inDirN, sampN)
		out = '%s/%s.indels.out' % (outDirN, sampN)
		vcf = '%s/%s.indels.vcf' % (outDirN, sampN)
		log = '%s/%s.somaticindeldetector.log' %  (outDirN, sampN)

		cmd = '%s --input_file:tumor %s -o %s --verboseOutput %s > %s' % (cmd, ibam, vcf, out, log)
		print cmd
		os.system(cmd)

		intvl = '%s/%s.indels.intervals' % (outDirN, sampN)
		cmd = 'awk \'OFS="\\t" {print $1":"$2-5"-"$3+5}\' %s > %s' % (out, intvl)
		print cmd
		os.system(cmd)

		annot_cmd = 'java -Xmx8g -jar /home/tools/GATK/GenomeAnalysisTK.jar -T VariantAnnotator -R %s --dbsnp %s --comp:KGPF %s --comp:ESPF %s -dcov 50000' % (ref, dbsnp, kgpf, espf)
		annot_vcf = '%s/%s.indels_annot.vcf' % (outDirN, sampN)
		annot_cmd = '%s -I %s --variant %s -o %s -L %s >> %s' % (annot_cmd, ibam, vcf, annot_vcf, intvl, log)
		print annot_cmd
		os.system(annot_cmd)

		flt_vcf = '%s/%s.indels_filter.vcf' % (outDirN, sampN)
		flt_out = '%s/%s.indels_filter.out' % (outDirN, sampN)
		filter_indel.filter_indel_single(annot_vcf, flt_vcf, flt_out)

		os.system('cut -f 1 %s | uniq >> %s' % (flt_out, log))

def paired_mode(tbam, nbam, outDirN, sampN, pl='CS', genome='hg19', server='smc1', pbs=False):
	ref = mysetting.ucscRefH[server][genome]
	dbsnp = mysetting.dbsnpH[server][genome]
	kgpf = mysetting.all_1kgH[server][genome]
	espf = mysetting.espH[server][genome]
	cosmic = mysetting.cosmicH[server][genome]

	cov = '-filter \'T_COV<%s\' -filter \'N_COV<%s\' -filter \'T_CONS_CNT<%s\'' % (COV_H[pl], COV_H[pl], CNT_H[pl])
	opt = '-filter \'T_INDEL_F<0.01\' %s -filter \'T_INDEL_CF<0.7\' -dcov 50000 --maxNumberOfReads 50000 --min_mapping_quality_score 15' % cov
	flt = '-rf DuplicateRead --filter_mismatching_base_and_quals -rf BadMate -rf UnmappedRead -rf NotPrimaryAlignment -rf MappingQualityUnavailable -rf MappingQuality'

	out = '%s/%s.indels_pair.out' % (outDirN, sampN)
	vcf = '%s/%s.indels_pair.vcf' % (outDirN, sampN)
	log = '%s/%s.somaticindeldetector_pair.log' % (outDirN, sampN)

	cmd = 'java -Xmx8g -jar /home/tools/GATK-2.2/GenomeAnalysisTK.jar -T SomaticIndelDetector -R %s %s %s' % (ref, opt, flt)
	cmd = '%s --input_file:normal %s --input_file:tumor %s -o %s --verboseOutput %s > %s' % (cmd, nbam,tbam, vcf,out, log)
	print cmd
	os.system(cmd)

	intvl = '%s/%s.indels_pair.intervals' % (outDirN, sampN)
	cmd = 'awk \'OFS="\\t" {print $1":"$2-5"-"$3+5}\' %s > %s' % (out, intvl)
	print cmd
	os.system(cmd)

	annot_cmd = 'java -Xmx8g -jar /home/tools/GATK/GenomeAnalysisTK.jar -T VariantAnnotator -R %s --dbsnp %s --comp:KGPF %s --comp:ESPF %s -dcov 50000' % (ref, dbsnp, kgpf, espf)
	annot_vcf = '%s/%s.indels_pair_annot.vcf' % (outDirN, sampN)
	annot_cmd = '%s -I %s --variant %s -o %s -L %s >> %s' % (annot_cmd, tbam, vcf, annot_vcf, intvl, log)
	print annot_cmd
	os.system(annot_cmd)
	
	flt_vcf = '%s/%s.indels_pair_filter.vcf' % (outDirN, sampN)
	flt_out = '%s/%s.indels_pair_filter.out' % (outDirN, sampN)
	filter_indel.filter_indel_paired(annot_vcf, flt_vcf, flt_out)

if __name__ == '__main__':
	paired_mode('/EQL5/pipeline/CS_mut/IRCR_GBM14_504_T03_CS/IRCR_GBM14_504_T03_CS.recal.bam','/EQL5/pipeline/CS_mut/IRCR_GBM14_504_B_CS/IRCR_GBM14_504_B_CS.recal.bam', '.', 'IRCR_GBM14_504_T_CS')
#	single_mode('/EQL5/pipeline/CS_mut/IRCR_GBM14_416_T_CS', '/home/ihlee/haha')
	##batch test for cancerscan
#	dirL = filter(lambda x: os.path.isdir('/EQL5/pipeline/CS_mut/' + x), os.listdir('/EQL5/pipeline/CS_mut'))
#	for dir in dirL:
#		baseDir = '/EQL5/pipeline/CS_mut/%s' % dir
#		print baseDir
#		single_mode(baseDir, baseDir)

	#batch single mode run for exome
#	for dir in mysetting.wxsBamDirL[:-1]+mysetting.oldPipelineL + ['/EQL1/NSL/exome_bam/bam_link']:
#		if 'somatic_mutect' in dir:
#			continue
#		single_mode(dir,'/EQL4/pipeline/indel_batch','SS')
#		for d in filter(lambda x: os.path.isdir(dir+'/'+x), os.listdir(dir)):
#			single_mode(dir+'/'+d,'/EQL4/pipeline/indel_batch','SS')
#
