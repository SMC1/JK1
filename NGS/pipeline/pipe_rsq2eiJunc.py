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

		inputFileN = inputFileP.split('/')[-1]
		sampN = inputFileN.split('_splice')[0]
		
		if sampN[1:4] not in ['096','145']:
			continue
		
		if pbs:
			os.system('echo "python ~/JK1/NGS/pipeline/pipe_s_rsq2eiJunc.py -i %s -n %s -p %s -c %s" | qsub -N %s -o %s/%s.Rsq_eiJunc.qlog -j oe' % \
			(inputFileP, sampN, projectN, False, sampN, storageBase+projectN+'/'+sampN, sampN))	

		else:
			os.system('(python ~/JK1/NGS/pipeline/pipe_s_rsq2eiJunc.py -i %s -n %s -p %s -c %s) 2> %s/%s.Rsq_eiJunc.qlog' % \
			(inputFileP, sampN, projectN, False, storageBase+projectN+'/'+sampN, sampN))	


#main(glob('/pipeline/fusion_test/*/*splice.gsnap'), projectN='test_ei', clean=False, pbs=True)
main(glob('/pipeline/RNAseq_fusion_096_145/*/*splice.gsnap'), projectN='RNAseq_eiJunc_096_145', clean=False, pbs=True)
#main(glob('/pipeline/RNAseq_fusion_FGFR/*/*splice.gsnap'), projectN='RNAseq_eiJunc_FGFR', clean=False, pbs=True)
