#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mypipe, mysetting
from glob import glob

## SYSTEM CONFIGURATION

def main(inputFilePathL, projectN, clean=False, pbs=False, server='smc1', genome='hg19'):
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

		inputFileP2 = inputFileP[:-7] + '\*.fq.gz'
		inputFileN = inputFileP.split('/')[-1]
		sampN = inputFileN.split('.')[0]

#		if sampN not in ['IRCR_GBM10_002_T_SS','IRCR_GBM14_399_T_SS','IRCR_GBM14_491_T_SS']:
#		if sampN[:14] not in ['IRCR_GBM10_002','IRCR_GBM14_410','IRCR_GBM14_505','IRCR_GBM14_553','IRCR_GBM14_570','IRCR_GBM13_225','IRCR_GBM14_630']:
		if sampN[:14] not in ['IRCR_GBM11_117']:
			continue

		print sampN, inputFileP2
		cmd = '/usr/bin/python %s/NGS/pipeline/pipe_s_xsq2mut.py -i %s -n %s -p %s -c %s -s %s -g %s' % (mysetting.SRC_HOME, inputFileP2, sampN, projectN, False, server, genome)

		if pbs:
			log = '%s/%s.Xsq.qlog' % (storageBase+projectN+'/'+sampN,sampN)
			os.system('echo "%s" | qsub -q %s -N %s -o %s -j oe' % (cmd, server, sampN, log))
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
#main(glob('/EQL2/SGI_20140128/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140103_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20140204/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140204_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20140210/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140210_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20140219/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140219_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20140331/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140331_xsq2mut', clean=False, pbs=True,server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20140410/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140410_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20140411/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140411_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/CS_20140327/WXS/fastq/link/*.1.fq.gz'), projectN='CS20140327_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/CS_20140430/WXS/fastq/link/*.1.fq.gz'), projectN='CS20140430_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/CS_20140512/WXS/fastq/link/*.1.fq.gz'), projectN='CS20140512_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/CS_20140513/WXS/fastq/link/*.1.fq.gz'), projectN='CS20140513_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
##sample from other cancer
#main(glob('/EQL2/150T/link/*.1.fq.gz'), projectN='CR_150_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/CS_HAPMAP/WXS/fastq/link/*.1.fq.gz'), projectN='CS_HAPMAP20', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20140526/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140526_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/CS_20140526/WXS/fastq/link/*.1.fq.gz'), projectN='CS20140526_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20140428/WXS/fastq/link/*.1.fq.gz'), projectN='JKM20140428_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20140529/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140529_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20140602/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140602_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/CS_20140519/WXS/fastq/link/*.1.fq.gz'), projectN='CS20140519_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20140611/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140611_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/CS_20140613/WXS/fastq/link/*.1.fq.gz'), projectN='CS20140613_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20140617/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140617_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20140625/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140625_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#samples from colon cancer
#main(glob('/EQL5/SignetRingCell/link/*.1.fq.gz'), projectN='SignetRingCell_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL5/Young_CRC/link/*.1.fq.gz'), projectN='Young_CRC_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140707/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140707_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20140714/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140714_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20140721/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140721_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20140728/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140728_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140804/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140804_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140807/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140807_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140811/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140811_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140813/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140813_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140818/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140818_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140825/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140825_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140827/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140827_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140901/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140901_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140904/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140904_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140917/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140917_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140930/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140930_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140930_NSC/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20140930_NSC_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20141001/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20141001_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20141008/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20141008_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20141021/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20141021_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20141027/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20141027_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20141103/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20141103_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20141110/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20141110_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20141112/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20141112_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20141126/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20141126_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20141202/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20141202_xsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20141210/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20141210_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20141218/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20141218_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20150102/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20150102_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20150112/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20150112_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20150115/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20150115_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20150121/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20150121_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20150123/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20150123_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20150128/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20150128_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20150206/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20150206_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
main(glob('/EQL2/SGI_20150223/WXS/fastq/link/*.1.fq.gz'), projectN='SGI20150223_xsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')

## tcga processing (with validation data)
#for sampN in ['TCGA-02-0003','TCGA-02-0055','TCGA-06-0145','TCGA-06-0184','TCGA-06-0190-T02','TCGA-06-0195','TCGA-06-0209']: ## first try
#for sampN in ['TCGA-06-0125','TCGA-06-0137','TCGA-06-0646','TCGA-06-0185','TCGA-06-0190-T01','TCGA-06-0190-B','TCGA-06-0124','TCGA-06-0169','TCGA-06-0213','TCGA-12-0619','TCGA-02-0033','TCGA-02-0047','TCGA-06-0141','TCGA-06-0157','TCGA-06-0173','TCGA-06-0178','TCGA-06-0187','TCGA-06-0122','TCGA-06-0126','TCGA-06-0128','TCGA-06-0142','TCGA-06-0151','TCGA-06-0171','TCGA-06-0188','TCGA-12-0616','TCGA-06-0189','TCGA-06-0237','TCGA-06-0238','TCGA-06-0241','TCGA-06-0644','TCGA-12-0618','TCGA-06-0129','TCGA-06-0130','TCGA-06-0158','TCGA-06-0168','TCGA-06-0174','TCGA-06-0139','TCGA-06-0152','TCGA-06-0166','TCGA-06-0645','TCGA-12-0615','TCGA-06-0165','TCGA-06-0167','TCGA-06-0214','TCGA-06-0219','TCGA-06-0648','TCGA-08-0386']:
#	main(glob('/EQL9/TCGA_WXS/fqgz/*%s*.1.fq.gz' % sampN), projectN='TCGA_T', clean=False, pbs=True, server='smc2', genome='hg19')
#	main(glob('/EQL10/TCGA_WXS/fqgz/*%s*.1.fq.gz' % sampN), projectN='TCGA_B', clean=False, pbs=True, server='smc2', genome='hg19')

## tcga processing (the rest)
doneL = ['TCGA-02-0003','TCGA-02-0055','TCGA-06-0145','TCGA-06-0184','TCGA-06-0190-T02','TCGA-06-0195','TCGA-06-0209']
doneL += ['TCGA-06-0125','TCGA-06-0137','TCGA-06-0646','TCGA-06-0185','TCGA-06-0190-T01','TCGA-06-0190-B','TCGA-06-0124','TCGA-06-0169','TCGA-06-0213','TCGA-12-0619','TCGA-02-0033','TCGA-02-0047','TCGA-06-0141','TCGA-06-0157','TCGA-06-0173','TCGA-06-0178','TCGA-06-0187','TCGA-06-0122','TCGA-06-0126','TCGA-06-0128','TCGA-06-0142','TCGA-06-0151','TCGA-06-0171','TCGA-06-0188','TCGA-12-0616','TCGA-06-0189','TCGA-06-0237','TCGA-06-0238','TCGA-06-0241','TCGA-06-0644','TCGA-12-0618','TCGA-06-0129','TCGA-06-0130','TCGA-06-0158','TCGA-06-0168','TCGA-06-0174','TCGA-06-0139','TCGA-06-0152','TCGA-06-0166','TCGA-06-0645','TCGA-12-0615','TCGA-06-0165','TCGA-06-0167','TCGA-06-0214','TCGA-06-0219','TCGA-06-0648','TCGA-08-0386', 'TCGA-06-5410']
#for fileN in glob('/EQL10/TCGA_WXS/fqgz/*.1.fq.gz'):
#	fid = re.match('(.*)-B.1.fq.gz', os.path.basename(fileN)).group(1)
##	if fid not in doneL and '-02-' in fid:
#	if fid not in doneL and '-06-' in fid:
#		if os.path.isdir('/EQL10/TCGA_WXS/TCGA_B/%s-B' % fid):
#			continue
#		print fid, os.path.basename(fileN)
#		main(glob('/EQL9/TCGA_WXS/fqgz/*%s*.1.fq.gz' % fid), projectN='TCGA_T', clean=False, pbs=True, server='smc2', genome='hg19')
#		main(glob('/EQL10/TCGA_WXS/fqgz/*%s*.1.fq.gz' % fid), projectN='TCGA_B', clean=False, pbs=True, server='smc2', genome='hg19')
