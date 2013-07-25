#!/usr/bin/python

import sys, os, re, getopt
import mybasic
from glob import glob

## SYSTEM CONFIGURATION

storageBase = '/pipeline/'
apacheBase = '/var/www/html/pipeline/'

def main(inputFilePathL, projectN, clean=False, pbs=False):

	if glob(storageBase+projectN):
		print ('File directory: already exists')
	else:
		os.system('mkdir %s/%s; \
			chmod a+w %s/%s' % (storageBase,projectN, storageBase,projectN))
		print('File directory: created')
	
	if glob(apacheBase+projectN):
		print ('Log directory: already exists')
	else:
		os.system('mkdir %s/%s; \
			chmod a+w %s/%s' % (apacheBase,projectN, apacheBase,projectN))
		print('Log directory: created')

	for inputFileP in inputFilePathL:

		inputFileP2 = inputFileP[:-7] + '\*.fq.gz'
		inputFileN = inputFileP.split('/')[-1]
		sampN = inputFileN.split('.')[0]

		if sampN[1:4] not in ['437']:  #,'453','559','775']:
			continue

		if pbs:
			os.system('echo "python ~/JK1/NGS/pipeline/pipe_s_xsq2mut.py -i %s -n %s -p %s -c %s" | qsub -N %s -o %s/%s.Xsq.qlog -j oe' % \
				(inputFileP2, sampN, projectN, False, sampN, storageBase+projectN+'/'+sampN, sampN))	

		else:
			os.system('(python ~/JK1/NGS/pipeline/pipe_s_xsq2mut.py -i %s -n %s -p %s -c %s) 2> %s/%s.Xsq.qlog' % \
				(inputFileP2, sampN, projectN, False, storageBase+projectN+'/'+sampN, sampN))	
			#os.system('(python ~/JK1/NGS/pipeline/pipe_s_xsq2mut.py -i %s -n %s -p %s -c %s)' % \
			#	(inputFileP, sampN, projectN, False))	


#main(glob('/home/heejin/practice/gatk/pipe_test/*.bam'), projectN='xsq_pipe_test2', clean=False, pbs=True)
main(glob('/EQL1/NSL/WXS/fastq/20130719/*.1.fq.gz'), projectN='ExomeSeq_20130723', clean=False, pbs=True)
