#!/usr/bin/python

import sys, os, re
import vep_mutect

def main(inDirNameL, postfix='_mutect.vcf', fork=False):
	inFileL = []

	for inDirName in inDirNameL:
		inFileL += filter(lambda x: 'backup' not in x, map(lambda x: x.rstrip(), os.popen('find %s -name *S%s' % (inDirName,postfix)).readlines()))
	
	for inFile in inFileL:
		outDir = '/'.join(inFile.split('/')[:-1])
		vepOut = outDir + '/' + inFile.split('/')[-1] + '_vep.dat'
		if not os.path.isfile(vepOut):
			print inFile, outDir
			sampN = re.match('(.*)%s' % postfix, os.path.basename(inFile)).group(1)
#			if sampN not in ['IRCR_GBM14_431_T_CS','IRCR_GBM14_459_T01_CS','IRCR_GBM14_459_T02_CS','IRCR_GBM14_446_T_CS','IRCR_MBT14_160_T_CS','IRCR_LC14_320_T_CS']:
			if sampN not in ['IRCR_GBM14_414_T_SS']:
				continue
			print sampN, inFile
			vep_mutect.vep_mutect_old(inFile, outDir)
#			vep_mutect.vep_mutect_new(inFile, sampN, outDir, fork)
	
if __name__ == '__main__':
#	main(['/EQL1/NSL/exome_bam/mutation', '/EQL1/NSL/WXS/exome_20130529'])
	main(['/EQL3/pipeline/somatic_mutect'], postfix='.mutect')
#	main(['/EQL1/pipeline/CS20140618_xsq2mut'])
#	main(['/EQL2/pipeline/CS20140613_xsq2mut'])
#	main(['/EQL4/pipeline/CS20140623_xsq2mut'], fork=True)
	
#	main(['/EQL5/pipeline/CS_mut'], postfix='_mutect.vcf', fork=True)
#	main(['/EQL5/pipeline/CS_mut'], postfix='.indels_filter.vcf', fork=True)
