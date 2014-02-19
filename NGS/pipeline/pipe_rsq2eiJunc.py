#!/usr/bin/python

import sys, os, re, getopt
import mybasic
from glob import glob

## SYSTEM CONFIGURATION

from mypipe import storageBase
from mypipe import apacheBase

def main(inputFilePathL, projectN, clean=False, pbs=False, server='smc1', genome='hg19'):

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
		
#		if sampN[1:4] not in ['096','145']:
#			continue
		print sampN
		
		cmd = 'python ~/JK1/NGS/pipeline/pipe_s_rsq2eiJunc.py -i %s -n %s -p %s -c %s -s %s -g %s' % (inputFileP, sampN, projectN, False, server, genome)
		if pbs:
			log = '%s/%s.Rsq_eiJunc.qlog' % (storageBase+projectN+'/'+sampN,sampN)
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))

		else:
			log = '%s/%s.Rsq_eiJunc.qlog' % (storageBase+projectN,sampN)
			os.system('(%s) 2> %s' % (cmd, log))


#main(glob('/pipeline/fusion_test/*/*splice.gsnap'), projectN='test_ei', clean=False, pbs=True)
#main(glob('/pipeline/RNAseq_fusion_096_145/*/*splice.gsnap'), projectN='RNAseq_eiJunc_096_145', clean=False, pbs=True)
#main(glob('/pipeline/RNAseq_fusion_FGFR/*/*splice.gsnap'), projectN='RNAseq_eiJunc_FGFR', clean=False, pbs=True)
#main(glob('/pipeline/SGI20131031_rsq2mut/*/*gsnap.gz'), projectN='SGI20131031_rsq2eiJunc', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/pipeline/SGI20131212_rsq2mut/*/*gsnap.gz'), projectN='SGI20131212_rsq2eiJunc', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/pipeline/SGI20131226_rsq2mut/*/*gsnap.gz'), projectN='SGI20131226_rsq2eiJunc', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL3/pipeline/SGI20131212_rsq2mut/*/*gsnap.gz'), projectN='SGI20131212_rsq2eiJunc', clean=False, pbs=True, server='smc1', genome='hg19')
main(glob('/EQL2/pipeline/SGI20140204_rsq2mut/*/*gsnap.gz'), projectN='SGI20140204_rsq2eiJunc', clean=False, pbs=True, server='smc1', genome='hg19')
