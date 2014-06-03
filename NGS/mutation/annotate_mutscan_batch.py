#!/usr/bin/python

import sys, os, re, getopt
import mybasic

def annotate_mutscan_batch(inDirName, inFilePattern, outDirName):
	fileNameL = os.listdir(inDirName)
	fileNameL = filter(lambda x: re.match(inFilePattern, x), fileNameL)

	print 'Files: %s (%s)' % (fileNameL, len(fileNameL))

	sampNameL = list(set([re.match(inFilePattern, inputFile).group(1) for inputFile in fileNameL]))
	sampNameL.sort()

	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:
		vcf=outDirName + '/' + sampN + '.mutscan.vcf'
		mut=inDirName + '/' + sampN + '.mutscan'
		vep_out=outDirName + '/' + sampN + '.mutscan.vep'
		make_vcf(mut, vcf, sampN)
		os.system('perl /home/tools/VEP/variant_effect_predictor.pl --offline --no_progress --fork 5 --config /home/tools/VEP/vep_config --format vcf -i %s -o %s --vcf --no_stats &> %s/%s.vep.log' % (vcf, vep_out, outDirName,sampN))

def make_vcf(mutscanFN, vcfFN, sampN):
	mutscanF = open(mutscanFN)
	mutscanlines = mutscanF.readlines()
	mutscanF.close()
	vcfF = open(vcfFN, 'w')
	vcfF.write('##fileformat=VCFv4.1\n')
	vcfF.write('#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t%s\n' % (sampN))
	for line in mutscanlines:
		cols = line[:-1].split('\t')
		chr = cols[0]
		if chr[:3] == 'chr':
			chr = chr[3:]
		if chr.upper() == 'M':
			chr = 'MT'
		pos = cols[1]
		ref = cols[2]
		alt = cols[3]
		refN = cols[4]
		altN = cols[5]
		vcfF.write ('%s\t%s\t.\t%s\t%s\t.\t.\tREF_N=%s;ALT_N=%s;\tGT\t./.\n' % (chr, pos, ref, alt, refN, altN))

	vcfF.close()

if __name__ == '__main__':
	annotate_mutscan_batch('/pipeline/test_ini_rsq2mut2/S096_RSq', '(.*)\.mutscan$', '/pipeline/test_ini_rsq2mut2/S096_RSq')
