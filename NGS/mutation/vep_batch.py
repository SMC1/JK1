#!/usr/bin/python

import sys,os,re
import myvep
from glob import glob

def main(inDirNameL, filterout='REJECT', postfixL=['_mutect.vcf','.indels_filter.vcf'], fork=False):
	inFileL = []

	for inDirName in inDirNameL:
		for postfix in postfixL:
			fL = glob('%s/*%s' % (inDirName, postfix))
			if fL:
				inFileL += fL
	
	for inFile in inFileL:
		outDir = os.path.dirname(inFile)
		vepOut = outDir + '/' + os.path.basename(inFile).replace('.vcf','_vep.dat')
		sampN = ''
		for postfix in postfixL:
			rm = re.search('(.*)%s' % postfix, os.path.basename(inFile))
			if rm:
				sampN = rm.group(1)

		ndata = int(os.popen("wc -l %s| cut -d ' ' -f 1" % inFile).readline()) - int(os.popen("grep -c '^#' %s" % inFile).readline())
		if not os.path.isfile(vepOut) and ndata > 0:
			print sampN, inFile
			run_vep(inFile, sampN, outDir, filterout, fork)

def run_vep(inFileN, sampN, outDirName, filterout='', fork=False):
	fName = os.path.basename(inFileN).replace('.vcf','')
	vep_in = '%s/%s_vep_in' % (outDirName, fName)
	if filterout == '':
		os.system("sed -e 's/^chrM/MT/' -e 's/^chr//' %s > %s" % (inFileN, vep_in))
	else:
		os.system("sed -e 's/^chrM/MT/' -e 's/^chr//' %s | grep -v %s > %s" % (inFileN,filterout, vep_in))
	vep_out = '%s/%s_vep.vcf' % (outDirName, fName)
	outName = '%s/%s_vep.dat' % (outDirName, fName)
	log = '%s/%s_vep.log' % (outDirName, fName)

	if fork:
		doFork = '--fork 12'
	else:
		doFork = ''
	
	os.system('perl /home/tools/VEP/variant_effect_predictor.pl --no_progress --config /home/tools/VEP/vep_config %s -i %s --format vcf -o %s --vcf --no_stats > %s 2>&1' % (doFork, vep_in, vep_out, log))
	myvep.process_vep_vcf(vep_out, sampN, outName)

if __name__ == '__main__':
#	main(glob('/EQL3/pipeline/somatic_mutation/*SS'), postfixL=['.mutect_filter.vcf','.indels_pair_filter.vcf'], fork=True)
#	main(glob('/EQL3/pipeline/somatic_mutation/*S'), postfixL=['.mutect_filter.vcf','.indels_pair_filter.vcf'], fork=True)
#	main(glob('/EQL3/pipeline/somatic_mutation/*S'), postfixL=['.mutect_rerun_filter.vcf'], fork=True)
#	main(glob('/EQL3/pipeline/somatic_mutation/*S'), postfixL=['.mutect_rerun_filter.vcf','.mutect_filter.vcf','.mutect_pair_filter.vcf','.indels_pair_filter.vcf'], fork=True)
#	main(glob('/EQL5/pipeline/CS_mut/*CS'), postfixL=['.mutect_filter.vcf','.indels_filter.vcf'], fork=True)
	main(glob('/EQL5/pipeline/CS_mut/*CS'), postfixL=['.mutect_filter.vcf','.mutect_single_filter.vcf','.indels_filter.vcf','.indels_single_filter.vcf'], fork=True)
#	main(glob('/EQL3/pipeline/somatic_mutation_single/*S'), postfixL=['.mutect_single_filter.vcf','.indels_single_filter.vcf'], fork=True)

#	main(glob('/EQL7/pipeline/SGI20140930_xsq2mut/IRCR_GBM14_567_T_SS'), postfixL=['.mutect_filter.vcf'], fork=True)
#	main(glob('/EQL7/pipeline/*xsq2mut/*554_T*_SS'), postfixL=['.mutect_filter.vcf'], fork=True)
#	main(glob('/EQL7/pipeline/*xsq2mut/*562_T*_SS'), postfixL=['.mutect_filter.vcf'], fork=True)
#	main(['/EQL7/pipeline/old_pipeline_xsq2mut/S532_T_SS'], postfixL=['.mutect_filter.vcf','.indels_filter.vcf'], fork=True)
#	main(['/EQL7/pipeline/SGI20140818_xsq2mut/IRCR_GBM14_529_T_SS'], postfixL=['_mutect.vcf','.indels_filter.vcf'], fork=True)
#	main(['/EQL8/pipeline/SGI20140204_rsq2mut/IRCR_GBM_352_TL_RSq','/EQL8/pipeline/SGI20140204_rsq2mut/IRCR_GBM_352_TR_RSq','/EQL6/pipeline/SCS20140203_rsq2mut/IRCR.GBM-363-SM_Bulk_RSq','/EQL6/pipeline/SCS20140203_rsq2mut/IRCR.GBM-363-SD_Bulk_RSq'], postfixL=['_splice.vcf'], fork=True)
#	main(['/EQL4/pipeline/indel_batch'], fork=True)
#	main(glob('/EQL5/pipeline/Young_CRC_xsq2mut/*_T_*')+glob('/EQL5/pipeline/SignetRingCell_xsq2mut/*_T_*'), postfixL=['_mutect.vcf','.indels_pair_filter.vcf'], fork=True)
#	main(glob('/EQL4/pipeline/mutect_batch/*S'), filterout='REJECT',  postfixL=['_mutect.vcf'], fork=True)
