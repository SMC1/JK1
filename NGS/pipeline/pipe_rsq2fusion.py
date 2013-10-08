#!/usr/bin/python

import sys, os, re, getopt
import mybasic
from glob import glob

## SYSTEM CONFIGURATION

storageBase = '/pipeline/'
#apacheBase = '/var/www/html/pipeline/'
apacheBase = '/var/www/html/pipeline2/'

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
	
		if sampN[1:4] not in ['096','145']:
			continue
		
		if pbs:
			os.system('echo "python ~/JK1/NGS/pipeline/pipe_s_rsq2fusion.py -i %s -n %s -p %s -c %s" | qsub -N %s -o %s/%s.Rsq_fusion.qlog -j oe' % \
			(inputFileP2, sampN, projectN, False, sampN, storageBase+projectN+'/'+sampN, sampN))	

		else:
			os.system('(python ~/JK1/NGS/pipeline/pipe_s_rsq2fusion.py -i %s -n %s -p %s -c %s) 2> %s/%s.Rsq_fusion.qlog' % \
			(inputFileP2, sampN, projectN, False, storageBase+projectN+'/'+sampN, sampN))	


#main(glob('/home/heejin/practice/gatk/pipe_test/*.bam'), projectN='rsq_pipe_test2', clean=False, pbs=True)
main(glob('/EQL1/NSL/RNASeq/fastq/link/*.1.fq.gz'), projectN='RNAseq_fusion_096_145', clean=False, pbs=True)
