#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mysetting
from glob import glob

## SYSTEM CONFIGURATION

from mypipe import storageBase
from mypipe import apacheBase

def main(inputFilePathL, projectN, clean=False, pbs=False):
	storageBase = os.path.dirname(mypipe.prepare_baseDir(projectN, mkdir=False)) + '/'
	apacheBase = storageBase

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

		inputFileP2 = inputFileP[:-7] + '\*.fq'
		inputFileN = inputFileP.split('/')[-1]
		sampN = inputFileN.split('_splice')[0]
		
	#	if sampN[1:4] not in ['436','783']:
	#		continue
		
		if pbs:
			os.system('echo "/usr/bin/python %s/NGS/pipeline/pipe_s_rsq2eiJunc.py -i %s -n %s -p %s -c %s" | qsub -N %s -o %s/%s.Rsq_eiJunc.qlog -j oe' % \
			(mysetting.SRC_HOME, inputFileP2, sampN, projectN, False, sampN, storageBase+projectN+'/'+sampN, sampN))	

		else:
			os.system('(/usr/bin/python %s/NGS/pipeline/pipe_s_rsq2eiJunc.py -i %s -n %s -p %s -c %s) 2> %s/%s.Rsq_eiJunc.qlog' % \
			(mysetting.SRC_HOME, inputFileP2, sampN, projectN, False, storageBase+projectN+'/'+sampN, sampN))	


#main(glob('/pipeline/fusion_test/*/*splice.gsnap'), projectN='test_ei', clean=False, pbs=True)
main(glob('/EQL2/TCGA/LUAD/RNASeq/fastq/*.1.fastq'), projectN='RNAseq_20130806', clean=False, pbs=False)
