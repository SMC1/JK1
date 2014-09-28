#!/usr/bin/python

import os, sys, getopt, re, glob
import mybasic, mysetting

def main(inFileDir,outFileDir,pbs=False):

	inFileNameL = glob.glob('%s/*analysis.hg19*' % (inFileDir,))

	for inFileName in inFileNameL:

#		pId = sId[:12]

		rm = re.match('.*(TCGA.{24}).*',inFileName)

		sId = rm.group(1)

#		if int(sId[13:15])>=10:
#			continue
		
		print sId

		if pbs:

			os.system('echo "Rscript %s/Array/purity/absolute.r %s %s %s" | qsub -N %s -o %s/%s.absolute.qlog -j oe' \
			% (mysetting.SRC_HOME,inFileName,sId,outFileDir, sId, outFileDir,sId))

		else:
			os.system('Rscript %s/Array/purity/absolute.r %s %s %s &>> %s/%s.absolute.qlog' % (mysetting.SRC_HOME,inFileName,sId,outFileDir, outFileDir,sId))

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#	main(optH['-i'], optH['-o'])

main('/EQL1/TCGA/GBM/array_cn/seg_absolute','/EQL1/TCGA/GBM/array_cn/absolute_results',True)
