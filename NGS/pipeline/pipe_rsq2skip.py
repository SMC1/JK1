#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mypipe, mysetting
from glob import glob

## SYSTEM CONFIGURATION

def main(inputFilePathL, projectN, clean=False, pbs=False, server='smc1', genome='hg19', sampNL=[]):
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

		inputFileN = inputFileP.split('/')[-1]
		sampN = inputFileN.split('_splice')[0]
		
		if sampNL != [] and sampN not in sampNL:
			continue
		print sampN
		
		cmd = '/usr/bin/python %s/NGS/pipeline/pipe_s_rsq2skip.py -i %s -n %s -p %s -c %s -s %s -g %s' % (mysetting.SRC_HOME, inputFileP, sampN, projectN, False, server, genome)
		if pbs:
			log = '%s/%s.Rsq_skip.qlog' % (storageBase+projectN+'/'+sampN,sampN)
			os.system('echo "%s" | qsub -q %s -N %s -o %s -j oe' % (cmd, server, sampN, log))

		else:
			log = '%s/%s.Rsq_skip.qlog' % (storageBase+projectN,sampN)
			os.system('(%s) 2> %s' % (cmd, log))


#main(glob('/home/heejin/practice/gatk/pipe_test/*.bam'), projectN='rsq_pipe_test2', clean=False, pbs=True)
#main(glob('/pipeline/RNAseq_fusion_096_145/*/*splice.gsnap'), projectN='RNAseq_exonSkip_096_145', clean=False, pbs=True)
#main(glob('/pipeline/RNAseq_fusion_FGFR/*/*splice.gsnap'), projectN='RNAseq_exonSkip_FGFR', clean=False, pbs=True)
#main(glob('/pipeline/test_ini_rsq2mut/*/*gsnap.gz'), projectN='test_ini_rsq2skip', clean=False, pbs=False, server='smc1', genome='hg19')
#main(glob('/pipeline/SGI20131212_rsq2mut/*/*gsnap.gz'), projectN='SGI20131212_rsq2skip', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/pipeline/SGI20131226_rsq2mut/*/*gsnap.gz'), projectN='SGI20131226_rsq2skip', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL3/pipeline/SGI20131212_rsq2mut/*/*gsnap.gz'), projectN='SGI20131212_rsq2skip', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/pipeline/SGI20140204_rsq2mut/*/*gsnap.gz'), projectN='SGI20140204_rsq2skip', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL2/pipeline/SGI20140219_rsq2mut/*/*gsnap.gz'), projectN='SGI20140219_rsq2skip', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL6/pipeline/JKM20140314_bulk_rsq2mut/*/*gsnap.gz'), projectN='JKM20140314_bulk_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL6/pipeline/JKM20140314_SCS_RM_rsq2mut/*/*gsnap.gz'), projectN='JKM20140314_SCS_RM_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL6/pipeline/JKM20140314_SCS_RX_rsq2mut/*/*gsnap.gz'), projectN='JKM20140314_SCS_RX_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL6/pipeline/JKM20140314_SCS_RMX_rsq2mut/*/*gsnap.gz'), projectN='JKM20140314_SCS_RMX_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL2/pipeline/SGI20140331_rsq2mut/*/*gsnap.gz'), projectN='SGI20140331_rsq2skip', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL6/pipeline/SCS20140422_rsq2mut/*/*gsnap.gz'), projectN='SCS20140422_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL6/pipeline/SGI20140520_rsq2mut/*/*gsnap.gz'), projectN='SGI20140520_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL3/pipeline/SGI20140526_rsq2mut/*/*gsnap.gz'), projectN='SGI20140526_rsq2skip', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL3/pipeline/SGI20140602_rsq2mut/*/*gsnap.gz'), projectN='SGI20140602_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL4/pipeline/SGI20140620_rsq2mut/*/*gsnap.gz'), projectN='SGI20140620_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL4/pipeline/SGI20140702_rsq2mut/*/*gsnap.gz'), projectN='SGI20140702_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL4/pipeline/SGI20140710_rsq2mut/*/*gsnap.gz'), projectN='SGI20140710_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL4/pipeline/SGI20140716_rsq2mut/*/*gsnap.gz'), projectN='SGI20140716_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL4/pipeline/SGI20140723_rsq2mut/*/*gsnap.gz'), projectN='SGI20140723_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20140804_rsq2mut/*/*gsnap.gz'), projectN='SGI20140804_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20140811_rsq2mut/*/*gsnap.gz'), projectN='SGI20140811_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20140818_rsq2mut/*/*gsnap.gz'), projectN='SGI20140818_rsq2skip', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20140821_rsq2mut/*/*gsnap.gz'), projectN='SGI20140821_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20140829_rsq2mut/*/*gsnap.gz'), projectN='SGI20140829_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20140904_rsq2mut/*/*gsnap.gz'), projectN='SGI20140904_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20140922_rsq2mut/*/*gsnap.gz'), projectN='SGI20140922_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL8/pipeline/SignetRingCell_rsq2mut/*/*gsnap.gz'), projectN='SignetRingCell_rsq2skip', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL8/pipeline/Young_CRC_rsq2mut/*/*gsnap.gz'), projectN='Young_CRC_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20140930_rsq2mut/*/*gsnap.gz'), projectN='SGI20140930_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20141013_rsq2mut/*/*gsnap.gz'), projectN='SGI20141013_rsq2skip', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20141021_rsq2mut/*/*gsnap.gz'), projectN='SGI20141021_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20141027_rsq2mut/*/*gsnap.gz'), projectN='SGI20141027_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20141031_rsq2mut/*/*gsnap.gz'), projectN='SGI20141031_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20141103_rsq2mut/*/*gsnap.gz'), projectN='SGI20141103_rsq2skip', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20141117_rsq2mut/*/*gsnap.gz'), projectN='SGI20141117_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20141126_rsq2mut/*/*gsnap.gz'), projectN='SGI20141126_rsq2skip', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20141202_rsq2mut/*/*gsnap.gz'), projectN='SGI20141202_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20141203_rsq2mut/*/*gsnap.gz'), projectN='SGI20141203_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20141211_rsq2mut/*/*gsnap.gz'), projectN='SGI20141211_rsq2skip', clean=False, pbs=True, server='smc2', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20141218_rsq2mut/*/*gsnap.gz'), projectN='SGI20141218_rsq2skip', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20141222_rsq2mut/*/*gsnap.gz'), projectN='SGI20141222_rsq2skip', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20150102_rsq2mut/*/*gsnap.gz'), projectN='SGI20150102_rsq2skip', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20150121_rsq2mut/*/*gsnap.gz'), projectN='SGI20150121_rsq2skip', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20150206_rsq2mut/*/*gsnap.gz'), projectN='SGI20150206_rsq2skip', clean=False, pbs=True, server='smc1', genome='hg19')
#main(glob('/EQL8/pipeline/SGI20150306_rsq2mut/*/*gsnap.gz'), projectN='SGI20150306_rsq2skip', clean=False, pbs=True, server='smc1', genome='hg19')
sampL=['IRCR_BCA14_302_RSq','IRCR_GBM14_514_RSq','IRCR_GBM14_553_RSq','IRCR_GBM15_686_RSq','IRCR_GBM15_693_T03_RSq','IRCR_GBM15_694_T03_RSq','IRCR_GBM15_696_RSq','IRCR_GBM15_699_RSq','IRCR_GBM15_702_RSq','IRCR_GBM15_714_RSq','IRCR_MBT15_208_RSq','IRCR_MBT15_210_RSq','IRCR_RCC14_148_RSq']
main(glob('/EQL8/pipeline/SGI20150306_rsq2mut/*/*gsnap.gz'), projectN='SGI20150306_rsq2skip', clean=False, pbs=True, server='smc1', genome='hg19',sampNL=sampL)
