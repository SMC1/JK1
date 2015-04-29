#!/usr/bin/python

import sys, os, re
import mysetting, mypipe, mysetting
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
#		if sampN not in ['IRCR_GBM10_031_T_SS','IRCR_GBM11_107_T_SS','NS09_763_T_SS','IRCR_GBM14_587_T_SS','IRCR_GBM14_588_T_SS','NS09_737_T_SS','IRCR_GBM11_106_T_SS']:
#		if sampN not in ['IRCR_GBM14_629_T_SS','IRCR_GBM11_133_T_SS','IRCR_GBM12_181_T_SS','IRCR_GBM12_194_T_SS','NS07_466_T_SS']:
#		if sampN not in ['IRCR_GBM14_554_TA_SS','IRCR_GBM14_562_T_SS']:
#		if sampN not in ['NS10_809_T_SS','IRCR_GBM11_112_T_SS','IRCR_GBM14_596_T_SS','IRCR_GBM14_491_T_SS']:
#			continue

		if pool == 'SGI':
			flag = '--use_pool_sgi'
		elif pool == 'CS':
			flag = '--cancerscan'
		else:
			flag = '--use_pool_dlink'
		if not os.path.isdir(storageBase + projectN + '/' + sampN): ## if the sample had not beed processed already
			cmd = '/usr/bin/python %s/NGS/pipeline/pipe_s_xsq2cn.py -i %s -n %s -p %s -c %s -s %s -g %s %s' % (mysetting.SRC_HOME, inputFile, sampN, projectN, False, server, genome, flag)
			print sampN, cmd, storageBase
			if pbs:
				log = '%s/%s.Xsq2cn.qlog' % (storageBase+projectN+'/'+sampN,sampN)
				os.system('echo "%s" | qsub -q %s -N x2cn_%s -o %s -j oe' % (cmd, server, sampN, log))
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
	trioH = mypipe.read_trio(trioFileN, bamDirL, tidL)

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

			cmd = '/usr/bin/python %s/NGS/pipeline/pipe_s_xsq2cn.py -i %s -j %s -n %s -p %s -c %s -s %s -g %s' % (mysetting.SRC_HOME, tumor, normal, sampN, projectN, False, 'smc1', 'hg19')
			print cmd
			if pbs:
				log = '%s/%s.Xsq2cn.qlog' % (storageBase+projectN+'/'+sampN,sampN)
				os.system('echo "%s" | qsub -q %s -N x2cn_%s -o %s -j oe' % (cmd, server, sampN, log))
			else:
				log = '%s/%s.Xsq2cn.qlog' % (storageBase+projectN, sampN)
				os.system('(%s) 2> %s' % (cmd, log))
	
		if trioH[tid]['recur_id'] != []:
			for recur in range(len(trioH[tid]['Recurrent'])):
				sampN = trioH[tid]['recur_id'][recur]
				tumor = trioH[tid]['Recurrent'][recur]
				normal = trioH[tid]['Normal'][0]
				cmd = '/usr/bin/python %s/NGS/pipeline/pipe_s_xsq2cn.py -i %s -j %s -n %s -p %s -c %s -s %s -g %s' % (mysetting.SRC_HOME, tumor, normal, sampN, projectN, False, 'smc1', 'hg19')
				print cmd
				if pbs:
					log = '%s/%s.Xsq2cn.qlog' % (storageBase+projectN+'/'+sampN,sampN)
					os.system('echo "%s" | qsub -q %s -N x2cn_%s -o %s -j oe' % (cmd, server, sampN, log))
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
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['65','66','67'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['68','69','70','71'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['72','73'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['74','75','76','77'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['60','64','78','79','80'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['81'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['59','60','63','78','79','82'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['64','80','83','84'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['63','74'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['85','86'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['74','78'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['87','88'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['87','89','90','91','92'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['93','94','95','96'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['98','99','100'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['99','101'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['102','103','104','105'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['97','106','107','108','109','110','111'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['112','113','114','115','116','117','118','119','120','121','122','123'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['124'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['87'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['37'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['125','126'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['125'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['127'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['128','129','130'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['131'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['132'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['90','133','134','135','138','139','140','141','142'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['136','137'], clean=False, pbs=True, server='smc1', genome='hg19')
	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='CNA', tidL=['143','144'], clean=False, pbs=True, server='smc1', genome='hg19')

#	pooled(inputFileL=glob('/EQL7/pipeline/SGI20140930_xsq2mut/IRCR_GBM14_571_T_*/*recal.bam'), projectN='CNA', pool='SGI', clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL7/pipeline/SGI20141021_xsq2mut/*/*recal.bam'), projectN='CNA', pool='SGI', clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL7/pipeline/SGI20141027_xsq2mut/*/*recal.bam'), projectN='CNA', pool='SGI', clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL7/pipeline/SGI20141103_xsq2mut/*/*606_T*recal.bam'), projectN='CNA', pool='SGI', clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL7/pipeline/SGI20141112_xsq2mut/*/*007_T*recal.bam'), projectN='CNA', pool='SGI', clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL7/pipeline/SGI20141112_xsq2mut/*/*756_T*recal.bam'), projectN='CNA', pool='SGI', clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL7/pipeline/SGI20141126_xsq2mut/*/*recal.bam'), projectN='CNA', pool='SGI', clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL7/pipeline/SGI20141202_xsq2mut/*/*recal.bam'), projectN='CNA', pool='SGI', clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL7/pipeline/SGI20141110_xsq2mut/*/*554_T*recal.bam'), projectN='CNA', pool='SGI', clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL7/pipeline/SGI20141112_xsq2mut/*/*562_T*recal.bam'), projectN='CNA', pool='SGI', clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL7/pipeline/SGI20141210_xsq2mut/*/*648_T*recal.bam'), projectN='CNA', pool='SGI', clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL7/pipeline/SGI20141218_xsq2mut/*/*recal.bam'), projectN='CNA', pool='SGI', clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL7/pipeline/SGI20150112_xsq2mut/*/NS05_188_T*recal.bam'), projectN='CNA', pool='SGI', clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL7/pipeline/SGI20150121_xsq2mut/*/*recal.bam'), projectN='CNA', pool='SGI', clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL1/pipeline/SGI20150128_xsq2mut/*/IRCR_GBM14_599_T*recal.bam'), projectN='CNA', pool='SGI', clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN = '/EQL5/pipeline/Young_pair_info.txt', projectN='CRC_xsq2cn', tidL=[], clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL2/pipeline/CS20140613_xsq2mut/*/*recal.bam'), projectN='CNA', pool='CS', clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL1/pipeline/CS20140618_xsq2mut/*/*recal.bam'), projectN='CNA', pool='CS', clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL4/pipeline/CS20140623_xsq2mut/*/*recal.bam'), projectN='CNA', pool='CS', clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL1/pipeline/CS20140618_xsq2mut/S141*/*recal.bam'), projectN='CS_CNA_test', pool='CS', clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL5/pipeline/CS_mut/*/*recal.bam'), projectN='CS_CNA', pool='CS', clean=False, pbs=True, server='smc1', genome='hg19')
#	pooled(inputFileL=glob('/EQL5/pipeline/CS_mut/*/*recal.bam'), projectN='CS_CNA', pool='CS', clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/home/ihlee/JK1/NGS/pipeline/PC_NS14_001TL_info.txt', projectN='CNA', tidL=['1'], clean=False, pbs=True, server='smc1', genome='hg19')
