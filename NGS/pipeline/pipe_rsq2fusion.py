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
		print sampN
	
#		if sampN[1:4] not in ['096','145']:
#			continue
		
		cmd = 'python ~/JK1/NGS/pipeline/pipe_s_rsq2fusion.py -i %s -n %s -p %s -c %s -s %s -g %s' % (inputFileP, sampN, projectN, False, server, genome)
		if pbs:
			log = '%s/%s.Rsq_fusion.qlog' % (storageBase+projectN+'/'+sampN,sampN)
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))

		else:
			log = '%s/%s.Rsq_fusion.qlog' % (storageBase+projectN,sampN)
			os.system('(%s) 2> %s' % (cmd, log))


#main(glob('/home/heejin/practice/gatk/pipe_test/*.bam'), projectN='rsq_pipe_test2', clean=False, pbs=True)
#main(glob('/EQL1/NSL/RNASeq/fastq/link/*.1.fq.gz'), projectN='RNAseq_fusion_096_145', clean=False, pbs=True)
#main(glob('/pipeline/test_ini_rsq2mut/*/*gsnap.gz'), projectN='test_ini_rsq2fusion', clean=False, pbs=False, server='smc1', genome='hg19')
#main(glob('/pipeline/SGI20131212_rsq2mut/*/*gsnap.gz'), projectN='SGI20131212_rsq2fusion', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/pipeline/SGI20131226_rsq2mut/*/*gsnap.gz'), projectN='SGI20131226_rsq2fusion', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL3/pipeline/SGI20131212_rsq2mut/*/*gsnap.gz'), projectN='SGI20131212_rsq2fusion', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/pipeline/SGI20140204_rsq2mut/*/*gsnap.gz'), projectN='SGI20140204_rsq2fusion', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/pipeline/SGI20140219_rsq2mut/*/*gsnap.gz'), projectN='SGI20140219_rsq2fusion', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL6/pipeline/JKM20140314_bulk_rsq2mut/*/*gsnap.gz'), projectN='JKM20140314_bulk_rsq2fusion', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL6/pipeline/JKM20140314_SCS_RM_rsq2mut/*/*gsnap.gz'), projectN='JKM20140314_SCS_RM_rsq2fusion', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL6/pipeline/JKM20140314_SCS_RX_rsq2mut/*/*gsnap.gz'), projectN='JKM20140314_SCS_RX_rsq2fusion', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL6/pipeline/JKM20140314_SCS_RMX_rsq2mut/*/*gsnap.gz'), projectN='JKM20140314_SCS_RMX_rsq2fusion', clean=False, pbs=True, server='smc2', genome='hg19')
main(glob('/EQL2/pipeline/SGI20140331_rsq2mut/*/*gsnap.gz'), projectN='SGI20140331_rsq2fusion', clean=False, pbs=True, server='smc1', genome='hg19')
