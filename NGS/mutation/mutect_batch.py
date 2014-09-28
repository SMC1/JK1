#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mysetting
from glob import glob

def mutect_pair(tBamN, nBamN, outDirN, genome='hg19', server='smc1', pbs=False):
	ref = mysetting.ucscRefH[server][genome]
	cosmic = mysetting.cosmicH[server][genome]
	dbsnp = mysetting.dbsnpH[server][genome]
	kgp = mysetting.all_1kgH[server][genome]
	esp = mysetting.espH[server][genome]

	sampN = re.search('(.*).recal.bam', os.path.basename(tBamN)).group(1)
	out = '%s/%s.mutect' % (outDirN,sampN)
	vcf_out = '%s/%s_mutect.vcf' % (outDirN,sampN)
	log = '%s/%s.mutect_pair.log' % (outDirN,sampN)
	cmd = 'java -Xmx8g -jar /home/tools/muTect/muTect.jar --analysis_type MuTect --tumor_f_pretest 0.005 --min_qscore 15 -dcov 50000 --fraction_contamination 0.005 --enable_extended_output'
	cmd = '%s --reference_sequence %s --cosmic %s --dbsnp %s --input_file:normal %s --input_file:tumor %s --out %s --vcf %s > %s' % (cmd, ref,cosmic,dbsnp, nBamN,tBamN, out,vcf_out, log)
	if not os.path.isfile(out):
		print cmd
		os.system(cmd)

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
		vcf = '%s/%s_mutect.vcf' % (mysetting.ctrMutectDir, sampN)
		log = '%s/%s.mutect_std.log' % (mysetting.ctrMutectDir, sampN)
		if glob('%s/%s.recal.bam' % (inDirName,sampN)):
			cmd = '%s --input_file:tumor %s -vcf %s --out %s > %s' % (cmd, ibam, vcf, out, log)
			print cmd
			os.system(cmd)

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
		vcf = '%s/%s_mutect.vcf' % (inDirName, sampN)
		log = '%s/%s.mutect_single.log' % (inDirName, sampN)
		if glob('%s/%s.recal.bam' % (inDirName,sampN)):
			cmd = '%s --input_file:tumor %s -vcf %s --out %s > %s' % (cmd, ibam, vcf, out, log)
			print cmd
			os.system(cmd)

if __name__ == '__main__':
	pass
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
