#!/usr/bin/python

import sys, os, re, getopt
import mypipe, mysetting
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

#		inputLogFileP = inputFileP.split('/')[:-1]
#
#		prosampNameL = list(set([re.match('.*/(.*).gsnap.qlog:Processed.*',line).group(1) for line in os.popen('grep Processed %s/*.qlog' % '/'.join(inputLogFileP))]))
		
		inputFileP2 = inputFileP[:-7] + '\*.fq.gz'
		inputFileN = inputFileP.split('/')[-1]
		sampN = inputFileN.split('.')[0]
		
#		if sampN[:14] in ['IRCR_GBM13_327','IRCR_GBM14_390','IRCR_GBM14_399','IRCR_GBM14_630','IRCR_GBM15_677','IRCR_MBT15_204','IRCR_MBT15_205']:
#		if sampN[:-4] in ['IRCR_LC14_440','IRCR_LC14_394','IRCR_LC14_423','IRCR_RCC14_148','IRCR_MBT15_206']:
#			continue

		print sampN
		cmd = '/usr/bin/python %s/NGS/pipeline/pipe_s_rsq2mut.py -i %s -n %s -p %s -c %s -s %s -g %s' % (mysetting.SRC_HOME, inputFileP2, sampN, projectN, False, server, genome)
		if pbs:
			log = '%s/%s.Rsq_mut.qlog' % (storageBase+projectN+'/'+sampN,sampN)
			os.system('echo "%s" | qsub -q %s -N %s -o %s -j oe' % (cmd, server, sampN, log))
		else:
			log = '%s/%s.Rsq_mut.qlog' % (storageBase+projectN,sampN)
			os.system('(%s) 2> %s' % (cmd, log))


#main(glob('/EQL6/NSL/HW/fastq/*.1.fq.gz'), projectN='HW_MBT_047T_rsq2mut', clean=False, pbs=False, server='smc1', genome='hg19')
#main(glob('/home/ihlee/test_data/test_rsq.1.fq.gz'), projectN='test_ini_rsq2mut', clean=False, pbs=False, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20131031/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20131031_rsq2mut', clean=False, pbs=True)
#main(glob('/home/heejin/practice/gatk/pipe_test/*.bam'), projectN='rsq_pipe_test2', clean=False, pbs=True)
#main(glob('/EQL1/NSL/RNASeq/align/splice_bam/*.bam'), projectN='RNAseq_17', clean=False, pbs=True)
#main(glob('/EQL2/SGI_20131212/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20131212_rsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20131226/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20131226_rsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20131212/RNASeq/fastq/link/S783*.1.fq.gz'), projectN='SGI20131212_rsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20140204/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20140204_rsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20140219/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20140219_rsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL6/RC85_LC195/fastq/Bulk_RSq/link/*.1.fq.gz'), projectN='JKM20140314_bulk_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL6/RC85_LC195/fastq/SCS_RM/link/*.1.fq.gz'), projectN='JKM20140314_SCS_RM_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL6/RC85_LC195/fastq/SCS_RMX/link/*.1.fq.gz'), projectN='JKM20140314_SCS_RMX_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL6/RC85_LC195/fastq/SCS_RX/link/*.1.fq.gz'), projectN='JKM20140314_SCS_RX_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL6/RC85_LC195/fastq/Bulk_RSq/link/*.1.fq.gz'), projectN='JKM20140314_bulk_mm10_rsq2mut', clean=False, pbs=True, server='smc1', genome='mm10')
#main(glob('/EQL2/SGI_20140331/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20140331_rsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL6/SGI_20140422_singlecell/RNASeq/fastq/link/*.1.fq.gz'), projectN='SCS20140422_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140526/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20140526_rsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20140520/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20140520_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140602/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20140602_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140620/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20140620_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140702/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20140702_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140710/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20140710_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140716/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20140716_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140723/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20140723_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140804/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20140804_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140811/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20140811_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140818/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20140818_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140821/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20140821_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140829/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20140829_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140904/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20140904_rsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20140922/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20140922_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL10/SignetRingCell_WTS/link/*.1.fq.gz'), projectN='SignetRingCell_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL10/Young_CRC_WTS/link/*.1.fq.gz'), projectN='Young_CRC_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20140930/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20140930_rsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20141013/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20141013_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20141021/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20141021_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20141027/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20141027_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20141031/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20141031_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20141103/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20141103_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20141117/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20141117_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20141126/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20141126_rsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20141202/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20141202_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20141203/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20141203_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20141211/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20141211_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20141218/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20141218_rsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20141222/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20141222_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/SGI_20150102/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20150102_rsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20150121/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20150121_rsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/SGI_20150206/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20150206_rsq2mut', clean=False, pbs=True, server='smc1', genome='hg19')
main(glob('/EQL2/SGI_20150306/RNASeq/fastq/link/*.1.fq.gz'), projectN='SGI20150306_rsq2mut', clean=False, pbs=True, server='smc2', genome='hg19')
