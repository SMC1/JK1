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

		inputLogFileP = inputFileP.split('/')[:-1]

		prosampNameL = list(set([re.match('.*/(.*).gsnap.qlog:Processed.*',line).group(1) for line in os.popen('grep Processed %s/*.qlog' % '/'.join(inputLogFileP))]))
		
		inputFileN = inputFileP.split('/')[-1]
		sampN = inputFileN.split('.')[0]
		
		if sampN[:8] not in prosampNameL:
			continue

		if sampN[1:4] not in ['671','740','592','660','586','428','642','460','568','372','608','572','618','458','594','453','775']:
			continue
		
		if pbs:
			os.system('echo "python ~/JK1/NGS/pipeline/pipe_s_rsq2mut.py -i %s -n %s -p %s -c %s" | qsub -N %s -o %s/%s.Rsq.qlog -j oe' % \
			(inputFileP, sampN, projectN, False, sampN, storageBase+projectN+'/'+sampN, sampN))	

		else:
			os.system('(python ~/JK1/NGS/pipeline/pipe_s_rsq2mut.py -i %s -n %s -p %s -c %s) 2> %s/%s.Rsq.qlog' % \
			(inputFileP, sampN, projectN, False, storageBase+projectN+'/'+sampN, sampN))	


#main(glob('/home/heejin/practice/gatk/pipe_test/*.bam'), projectN='rsq_pipe_test2', clean=False, pbs=True)
main(glob('/EQL1/NSL/RNASeq/align/splice_bam/*.bam'), projectN='RNAseq_17', clean=False, pbs=True)
