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

		inputFileP2 = inputFileP[:-7] + '\*.fq.gz'
		inputFileN = inputFileP.split('/')[-1]
		sampN = inputFileN.split('.')[0]

#		if sampN[1:4] not in ['096','145']:
#			continue
		print sampN

		cmd = 'python ~/JK1/NGS/pipeline/pipe_s_rsq2expr.py -i %s -n %s -p %s -c %s -s %s -g %s' % (inputFileP2, sampN, projectN, False, server, genome)
		if pbs:
			log = '%s/%s.Rsq_expr.qlog' % (storageBase+projectN+'/'+sampN,sampN)
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))

		else:
			log = '%s/%s.Rsq_expr.qlog' % (storageBase+projectN,sampN)
			os.system('(%s) 2> %s' % (cmd, log))


#main(glob('/home/heejin/practice/pipeline/fusion/*.1.fq.gz'), projectN='test_rpkm2', clean=False, pbs=True)
#main(glob('/EQL1/NSL/RNASeq/fastq/link/*.1.fq.gz'), projectN='RNAseq_expr_096_145', clean=False, pbs=True)
#main(glob('/EQL1/NSL/RNASeq/fastq/link/*.1.fq.gz'), projectN='RNAseq_fusion_FGFR', clean=False, pbs=True)
#main(glob('/EQL6/NSL/WY/fastq/link/*.1.fq.gz'), projectN='WY_RNASeq_expr', clean=False, pbs=True)
#main(glob('/home/ihlee/test_data/test_rsq*.1.fq.gz'), projectN='test_ini_rsq2expr', clean=False, pbs=False, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20131031/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20131031_rsq2expr', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20131119/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20131119_rsq2expr', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20131212/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20131212_rsq2expr', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20131226/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20131226_rsq2expr', clean=False, pbs=True, server='smc1', genome='hg19')
main(glob('/EQL2/SGI_20140204/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20140204_rsq2expr', clean=False, pbs=True, server='smc1', genome='hg19')
