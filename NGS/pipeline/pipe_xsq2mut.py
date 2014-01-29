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

#		if sampN[1:4] not in ['437']:# ,'453','559','775']:
#			continue

		print sampN
		cmd = '/usr/bin/python ~/JK1/NGS/pipeline/pipe_s_xsq2mut.py -i %s -n %s -p %s -c %s -s %s -g %s' % (inputFileP2, sampN, projectN, False, server, genome)
		if pbs:
			log = '%s/%s.Xsq.qlog' % (storageBase+projectN+'/'+sampN,sampN)
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))

		else:
			log = '%s/%s.Xsq.qlog' % (storageBase+projectN,sampN)
			os.system('(%s) 2> %s' % (cmd, log))


#main(glob('/home/heejin/practice/gatk/pipe_test/*.bam'), projectN='xsq_pipe_test2', clean=False, pbs=True)
#main(glob('/EQL1/NSL/WXS/fastq/20130719/*.1.fq.gz'), projectN='ExomeSeq_20130723', clean=False, pbs=True)
#main(glob('/EQL2/SGI_20131031/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20131031_xsq2mut', clean=False, pbs=True)
#main(glob('/home/ihlee/test_data/test_xsq*.1.fq.gz'), projectN='test_ini_xsq2mut', clean=False, pbs=False, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20131119/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20131119_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20131212/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20131212_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20131216/WXS/fastq/link/*.1.fq.gz'),projectN='SGI20131216_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20140103/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140103_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
main(glob('/EQL2/SGI_20140128/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140103_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
