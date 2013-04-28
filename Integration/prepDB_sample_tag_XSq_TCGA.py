#!/usr/bin/python

import sys, os, getopt, re
import mybasic


def main(dirPath):

	fileNameL = filter(lambda x: re.match('.*TCGA-..-....-0..*\.bam',x), os.listdir(dirPath)) # normal sample, bam
	fileNameTokL = map(lambda x: re.match('.*(TCGA-..-....)-...-..([DW]).*\.bam',x), fileNameL)

	h = {}

	for rm in fileNameTokL:

		sN = rm.group(1)
		type = rm.group(2)

		if 'SOLiD' in rm.group(0):
			type += '-SD'
		elif 'IlluminaGA' in rm.group(0):
			type += '-GA'

		mybasic.addHash(h,sN,type)

	for (sN,typeL) in h.iteritems():	
		typeL = list(set(typeL))
		typeL.sort()
		sys.stdout.write('%s\tXSeq_%s\n' % (sN,','.join(typeL)))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:t',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#
#	main(optH['-i'], optH['-o'])

main('/EQL4/TCGA/GBM/WXS/alignment')
