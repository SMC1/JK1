#!/usr/bin/python

import sys, os, re
import mysetting, mypipe
from glob import glob

# routine for unmatched samples
def pooled(inputFileL, projectN, pool='SGI', clean=False, pbs=False, server='smc1', genome='hg19'):
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

	for inputFile in inputFileL:

		inputFileN = inputFile.rstrip().split('/')[-1]
		sampN = inputFileN.split('.')[0]
		if 'KN' in sampN:
			continue
#		sId = re.match('.{1}(.*)_T.{,2}_[STKNC]{2}', sampN).group(1)
#		if sId not in ['437','453','559','671','775']: ## unmatched samples from DNA Link
#		if sId not in ['722','796','171','302','121','319','652','208','015','202','314','503','279','320','285','335','284','334','388','533','585','783','316','317','223','240','243','323','3A','3B','5A','5B','7A','7B','8A','8B','9A','9B','10A','10B','11A','11B','12A','12B','14A','14B']:
#		if sampN not in ['IRCR_GBM14_460_T_CS','IRCR_GBM14_460_B_CS']:
#		if sampN in os.listdir('/EQL5/pipeline/CS_CNA'):
#			continue

		if pool == 'SGI':
			flag = '--use_pool_sgi'
		elif pool == 'CS':
			flag = '--cancerscan'
		else:
			flag = '--use_pool_dlink'
		if not os.path.isdir(storageBase + projectN + '/' + sampN): ## if the sample had not beed processed already
			cmd = '/usr/bin/python ~/JK1/NGS/pipeline/pipe_s_xsq2cn.py -i %s -n %s -p %s -c %s -s %s -g %s %s' % (inputFile, sampN, projectN, False, server, genome, flag)
			print sampN, cmd, storageBase
			if pbs:
				log = '%s/%s.Xsq2cn.qlog' % (storageBase+projectN+'/'+sampN,sampN)
				os.system('echo "%s" | qsub -N x2cn_%s -o %s -j oe' % (cmd, sampN, log))
			else:
				log = '%s/%s.Xsq2cn.qlog' % (storageBase+projectN, sampN)
				os.system('(%s) 2> %s' % (cmd, log))

def main(trioFileN, projectN, tidL=[], clean=False, pbs=False, server='smc1', genome='hg19'):
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

	bamDirL = mysetting.wxsBamDirL
	trioH = mypipe.read_trio(trioFileN, bamDirL)

	## assume 1 primary & normal per trio
	for tid in trioH:
		if tidL != [] and tid not in tidL:
			continue
		if trioH[tid]['Normal'] == []:
			continue

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
					print cmd
					log = '%s/%s.Xsq2cn.qlog' % (storageBase+projectN+'/'+sampN,sampN)
					os.system('echo "%s" | qsub -N x2cn_%s -o %s -j oe' % (cmd, sampN, log))
				else:
					log = '%s/%s.Xsq2cn.qlog' % (storageBase+projectN, sampN)
					os.system('(%s) 2> %s' % (cmd, log))


if __name__ == '__main__':
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['37','43'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['51','52'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['53'], clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL1/pipeline/ExomeSeq_20130723/*/*_T_*recal.bam')+glob('/EQL1/NSL/exome_bam/bam_link/*_T_*recal.bam'), projectN='CNA', pool='DLink', clean=False, pbs=False, server='smc1', genome='hg19')
#	mylist = glob('/EQL3/pipeline/SGI20131119_xsq2mut/S4*/*_T_*recal.bam')+glob('/EQL3/pipeline/SGI20131119_xsq2mut/S6?_*/*_T_*recal.bam')+glob('/EQL3/pipeline/SGI20131119_xsq2mut/S752*/*recal.bam')+glob('/EQL3/pipeline/SGI20131119_xsq2mut/S148*/*recal.bam')
#	mylist = glob('/EQL2/pipeline/SGI*xsq2mut/*/*_T_*recal.bam') + glob('/EQL3/pipeline/SGI*xsq2mut/*/*_T_*recal.bam')
#	pooled(inputFileL=mylist, projectN='CNA_pool', pool='SGI', clean=False, pbs=False, server='smc1', genome='hg19')
#	cslist = glob('/EQL2/pipeline/CS*xsq2mut/*/*_T_*recal.bam') + glob('/EQL3/pipeline/CS*xsq2mut/*/*_T_*recal.bam')
#	pooled(inputFileL=cslist, projectN='CNA', pool='CS', clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['37'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['58'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['59'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['28'], clean=False, pbs=False, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['28'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['64'], clean=False, pbs=True, server='smc1', genome='hg19')
	main(trioFileN = '/EQL5/pipeline/Young_pair_info.txt', projectN='CRC_xsq2cn', tidL=[], clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL2/pipeline/CS20140613_xsq2mut/*/*recal.bam'), projectN='CNA', pool='CS', clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL1/pipeline/CS20140618_xsq2mut/*/*recal.bam'), projectN='CNA', pool='CS', clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL4/pipeline/CS20140623_xsq2mut/*/*recal.bam'), projectN='CNA', pool='CS', clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL1/pipeline/CS20140618_xsq2mut/S141*/*recal.bam'), projectN='CS_CNA_test', pool='CS', clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL5/pipeline/CS_mut/*/*recal.bam'), projectN='CS_CNA', pool='CS', clean=False, pbs=True, server='smc1', genome='hg19')
