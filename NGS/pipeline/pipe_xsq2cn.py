#!/usr/bin/python

import sys, os, re
import mysetting, mypipe
from glob import glob

## SYSTEM CONFIGURATION

from mypipe import storageBase
from mypipe import apacheBase

# routine for unmatched samples
def pooled(inputFileL, projectN, dirL=mysetting.poolB_SGI, clean=False, pbs=False, server='smc1', genome='hg19'):
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

	for inputFile in inputFileL:

		inputFileN = inputFile.rstrip().split('/')[-1]
		sampN = inputFileN.split('.')[0]
		if 'KN' in sampN:
			continue
		sId = re.match('.{1}(.*)_T_[STKN]{2}', sampN).group(1)
#		if sId not in ['437','453','559','671','775']: ## unmatched samples from DNA Link
#			continue

		flag = '--use_pool_dlink'
		cmd = '/usr/bin/python ~/JK1/NGS/pipeline/pipe_s_xsq2cn.py -i %s -n %s -p %s -c %s -s %s -g %s %s' % (inputFile, sampN, projectN, False, 'smc1', 'hg19', flag)
		if pbs:
			log = '%s/%s.Xsq2cn.qlog' % (storageBase+projectN+'/'+sampN,sampN)
			os.system('echo "%s" | qsub -N x2cn_%s -o %s -j oe' % (cmd, sampN, log))
		else:
			log = '%s/%s.Xsq2cn.qlog' % (storageBase+projectN, sampN)
			os.system('(%s) 2> %s' % (cmd, log))

def main(trioFileN, projectN, clean=False, pbs=False, server='smc1', genome='hg19'):
	bamDirL = mysetting.wxsBamDirL
	trioH = mypipe.read_trio(trioFileN, bamDirL)

	## assume 1 primary & normal per trio
	for tid in trioH:
#		if tid not in ['34','35','36']:
#			continue

		if trioH[tid]['prim_id'] != []:
			sampN = trioH[tid]['prim_id'][0]
			tumor = trioH[tid]['Primary'][0]
			normal = trioH[tid]['Normal'][0]

			cmd = '/usr/bin/python ~/JK1/NGS/pipeline/pipe_s_xsq2cn.py -i %s -j %s -n %s -p %s -c %s -s %s -g %s' % (tumor, normal, sampN, projectN, False, 'smc1', 'hg19')
			print cmd
			if pbs:
				log = '%s/%s.Xsq2cn.qlog' % (storageBase+projectN+'/'+sampN,sampN)
				os.system('echo "%s" | qsub -N x2cn_%s -o %s -j oe' % (cmd, sampN, log))
			else:
				log = '%s/%s.Xsq2cn.qlog' % (storageBase+projectN, sampN)
				os.system('(%s) 2> %s' % (cmd, log))
	
		if trioH[tid]['recur_id'] != []:
			for recur in range(len(trioH[tid]['Recurrent'])):
				sampN = trioH[tid]['recur_id'][recur]
				tumor = trioH[tid]['Recurrent'][recur]
				normal = trioH[tid]['Normal'][0]
				cmd = '/usr/bin/python ~/JK1/NGS/pipeline/pipe_s_xsq2cn.py -i %s -j %s -n %s -p %s -c %s -s %s -g %s' % (tumor, normal, sampN, projectN, False, 'smc1', 'hg19')
				print cmd
				if pbs:
					log = '%s/%s.Xsq2cn.qlog' % (storageBase+projectN+'/'+sampN,sampN)
					os.system('echo "%s" | qsub -N x2cn_%s -o %s -j oe' % (cmd, sampN, log))
				else:
					log = '%s/%s.Xsq2cn.qlog' % (storageBase+projectN, sampN)
					os.system('(%s) 2> %s' % (cmd, log))


if __name__ == '__main__':
	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', clean=False, pbs=True, server='smc1', genome='hg19')
##	pooled(inputFileL=glob('/EQL1/pipeline/ExomeSeq_20130723/*/*_T_*recal.bam')+glob('/EQL1/NSL/exome_bam/bam_link/*_T_*recal.bam'), projectN='CNA', dirL=mysetting.poolB_DLink, clean=False, pbs=True, server='smc1', genome='hg19')