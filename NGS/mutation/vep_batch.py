#!/usr/bin/python

import sys,os,re
import myvep
from glob import glob

def main(inDirNameL, postfixL=['_mutect.vcf','.indels_filter.vcf'], fork=False):
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
		if not os.path.isfile(vepOut):
			print sampN, inFile
			run_vep(inFile, sampN, outDir, fork)

def run_vep(inFileN, sampN, outDirName, fork=False):
	fName = os.path.basename(inFileN).replace('.vcf','')
	vep_in = '%s/%s_vep_in' % (outDirName, fName)
	os.system("sed -e 's/^chrM/MT/' -e 's/^chr//' %s > %s" % (inFileN, vep_in))
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
#	main(glob('/EQL5/pipeline/CS_mut/*CS'), fork=True)
#	main(['/EQL4/pipeline/indel_batch'], fork=True)
	main(glob('/EQL5/pipeline/Young_CRC_xsq2mut/*_T_*')+glob('/EQL5/pipeline/SignetRingCell_xsq2mut/*_T_*'), postfixL=['_mutect.vcf','.indels_pair_filter.vcf'], fork=True)
