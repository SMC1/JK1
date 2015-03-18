#!/usr/bin/python

import sys, os, re
import mysetting, mypipe, mysetting
from glob import glob

def tcga(tumorDirN, bloodDirN, projectN='TCGA_somatic', pbs=False, server='smc2', genome='hg19'):
	storageBase = os.path.dirname(mypipe.prepare_baseDir(projectN, mkdir=False)) + '/'
	apacheBase = storageBase
	if glob(storageBase+projectN):
		print ('File directory: already exists')
	else:
		os.system('mkdir %s/%s; \
			chmod a+w %s/%s' % (storageBase,projectN, storageBase,projectN))
		print ('File directory: created')

	if glob(apacheBase+projectN):
		print ('Log directory: already exists')
	else:
		os.system('mkdir %s/%s; \
			chmod a+w %s/%s' % (apacheBase,projectN, apacheBase,projectN))
		print ('Log directory: created')

	for normalFileN in glob('%s/*/*recal.bam' % bloodDirN):
		sid = re.match('(.*)-B.recal.bam', os.path.basename(normalFileN)).group(1)
		tumorFileNL = glob('%s/*/%s*recal.bam' % (tumorDirN, sid))

		for tumorFileN in tumorFileNL:
			tid = re.match('(.*)\.recal.bam$', os.path.basename(tumorFileN)).group(1)
			if not os.path.isdir('%s/%s/%s' % (storageBase, projectN, tid)):
				cmd = '/usr/bin/python %s/NGS/pipeline/pipe_s_xsq2somatic.py -i %s -j %s -n %s -p %s -c %s -s %s -g %s' % (mysetting.SRC_HOME, tumorFileN, normalFileN, tid, projectN, False, server, genome)
				print cmd

				if pbs:
					log = '%s/%s.Xsq2somatic.qlog' % (storageBase+projectN+'/'+tid,tid)
					os.system('echo "%s" | qsub -q %s -N x2somatic_%s -o %s -j oe' % (cmd, server, tid, log))
				else:
					log = '%s/%s.Xsq2somatic.qlog' % (storageBase+projectN, tid)
					os.system('(%s) 2> %s' % (cmd, log))
			#if not done
		#for tumorFileN
	# for normalFileN

def single(inputFilePathL, projectN, clean=False, pbs=False, server='smc1', genome='hg19'):
	storageBase = os.path.dirname(mypipe.prepare_baseDir(projectN, mkdir=False)) + '/'
	apacheBase = storageBase
	if glob(storageBase+projectN):
		print ('File directory: already exists')
	else:
		os.system('mkdir %s/%s; \
			chmod a+w %s/%s' % (storageBase,projectN, storageBase,projectN))
		print ('File directory: created')

	if glob(apacheBase+projectN):
		print ('Log directory: already exists')
	else:
		os.system('mkdir %s/%s; \
			chmod a+w %s/%s' % (apacheBase,projectN, apacheBase,projectN))
		print ('Log directory: created')
			
	for inputFileP in inputFilePathL:
		if '_B_' in inputFileP:
			continue
		inputFileN = os.path.basename(inputFileP)
		sampN = inputFileN.split('.')[0]
		
#		if sampN not in ['IRCR_GBM14_571_T_SS','IRCR_GBM10_031_T_SS','IRCR_GBM11_107_T_SS','NS09_763_T_SS','IRCR_GBM14_587_T_SS','IRCR_GBM14_588_T_SS','NS09_737_T_SS','IRCR_GBM11_106_T_SS','IRCR_GBM14_606_T_SS','IRCR_GBM14_554_TA_SS','IRCR_GBM10_007_T_SS','IRCR_GBM14_562_T_SS','NS09_756_T_SS','IRCR_GBM11_133_T_SS','IRCR_GBM12_181_T_SS','IRCR_GBM12_194_T_SS','NS07_466_T_SS','IRCR_GBM14_629_T_SS','IRCR_GBM14_648_T_SS']:
#		if sampN not in ['NS10_809_T_SS','IRCR_GBM11_112_T_SS','IRCR_GBM14_596_T_SS','IRCR_GBM14_491_T_SS']:
#			continue

		print sampN, inputFileP

		cmd = '/usr/bin/python %s/NGS/pipeline/pipe_s_xsq2somatic.py -i %s -n %s -p %s -c %s -s %s -g %s' % (mysetting.SRC_HOME, inputFileP, sampN, projectN, False, server, genome)
#		print cmd

		if pbs:
			log = '%s/%s.Xsq2somatic_s.qlog' % (storageBase+projectN+'/'+sampN,sampN)
			os.system('echo "%s" | qsub -q %s -N x2somatic_%s_s -o %s -j oe' % (cmd, server, sampN, log))
		else:
			log = '%s/%s.Xsq2somatic_s.qlog' % (storageBase+projectN, sampN)
			os.system('(%s) 2> %s' % (cmd, log))

def main(trioFileN, projectN, tidL=[], clean=False, pbs=False, server='smc1', genome='hg19'):
	storageBase = os.path.dirname(mypipe.prepare_baseDir(projectN, mkdir=False)) + '/'
	apacheBase = storageBase
	if glob(storageBase+projectN):
		print ('File directory: already exists')
	else:
		os.system('mkdir %s/%s; \
			chmod a+w %s/%s' % (storageBase,projectN, storageBase,projectN))
		print ('File directory: created')
	
	if glob(apacheBase+projectN):
		print ('Log directory: already exists')
	else:
		os.system('mkdir %s/%s; \
			chmod a+w %s/%s' % (apacheBase,projectN, apacheBase,projectN))
		print ('Log directory: created')
	
	bamDirL = mysetting.wxsBamDirL
	trioH = mypipe.read_trio(trioFileN, bamDirL, tidL)

	## assume 1 primary & normal per trio
	for tid in trioH:
		if tidL != [] and tid not in tidL:
			continue
		if trioH[tid]['Normal'] == []:
			continue
		
		if trioH[tid]['prim_id'] != []: ##primary
			sampN = trioH[tid]['prim_id'][0]
			print tid, trioH[tid]['Primary']
			tumor = trioH[tid]['Primary'][0]
			normal = trioH[tid]['Normal'][0]

			cmd = '/usr/bin/python %s/NGS/pipeline/pipe_s_xsq2somatic.py -i %s -j %s -n %s -p %s -c %s -s %s -g %s' % (mysetting.SRC_HOME, tumor, normal, sampN, projectN, False, server, genome)
			print cmd

			if pbs:
				log = '%s/%s.Xsq2somatic.qlog' % (storageBase+projectN+'/'+sampN,sampN)
				os.system('echo "%s" | qsub -q %s -N x2somatic_%s -o %s -j oe' % (cmd, server, sampN, log))
			else:
				log = '%s/%s.Xsq2somatic.qlog' % (storageBase+projectN, sampN)
				os.system('(%s) 2> %s' % (cmd, log))

		if trioH[tid]['recur_id'] != []: ##recurrent
			for recur in range(len(trioH[tid]['Recurrent'])):
				sampN = trioH[tid]['recur_id'][recur]
				tumor = trioH[tid]['Recurrent'][recur]
				normal = trioH[tid]['Normal'][0]
				cmd = '/usr/bin/python %s/NGS/pipeline/pipe_s_xsq2somatic.py -i %s -j %s -n %s -p %s -c %s -s %s -g %s' % (mysetting.SRC_HOME, tumor, normal, sampN, projectN, False, server, genome)
				print cmd
				if pbs:
					log = '%s/%s.Xsq2somatic.qlog' % (storageBase+projectN+'/'+sampN,sampN)
					os.system('echo "%s" | qsub -q %s -N x2somatic_%s -o %s -j oe' % (cmd, server, sampN, log))
				else:
					log = '%s/%s.Xsq2somatic.qlog' % (storageBase+projectN, sampN)
					os.system('(%s) 2> %s' % (cmd, log))

if __name__ == '__main__':
	#test
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['62'], clean=False, pbs=False, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['65','66','67'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['68','69','70','71'], clean=False, pbs=True, server='smc2', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['72'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['73'], clean=False, pbs=True, server='smc2', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['74','75','76','77'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['81'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['59','60','63','78','79','82'], clean=False, pbs=True, server='smc2', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['64','80','83','84'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['63','74'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['58'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['85','86'], clean=False, pbs=True, server='smc2', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['74','78'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['87'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['88'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['87','89','90','91','92'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['93','94','95','96'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['98','99','100'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['99','101'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['102','103','104','105'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['97','106','107','108','109','110','111'], clean=False, pbs=True, server='smc2', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['112','113','114','115','116','117','118','119','120','121','122','123'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['124'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['37'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['125','126'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['125'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['127'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['128','129','130'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['131'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['132'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['90','133','134','135','136','137','138','139','140','141','142'], clean=False, pbs=True, server='smc1', genome='hg19')
	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=['143','144'], clean=False, pbs=True, server='smc1', genome='hg19')

#	single(inputFilePathL=glob('/EQL7/pipeline/SGI20140930_xsq2mut/*/*recal.bam'), projectN='somatic_mutation_single', clean=False, pbs=True, server='smc2', genome='hg19')
#	single(inputFilePathL=glob('/EQL7/pipeline/SGI20141021_xsq2mut/*/*recal.bam'), projectN='somatic_mutation_single', clean=False, pbs=True, server='smc2', genome='hg19')
#	single(inputFilePathL=glob('/EQL7/pipeline/SGI20141027_xsq2mut/*/*recal.bam'), projectN='somatic_mutation_single', clean=False, pbs=True, server='smc2', genome='hg19')
#	single(inputFilePathL=glob('/EQL7/pipeline/SGI20141103_xsq2mut/*/*recal.bam'), projectN='somatic_mutation_single', clean=False, pbs=True, server='smc2', genome='hg19')
#	single(inputFilePathL=glob('/EQL7/pipeline/SGI20141110_xsq2mut/*/*recal.bam'), projectN='somatic_mutation_single', clean=False, pbs=True, server='smc2', genome='hg19')
#	single(inputFilePathL=glob('/EQL7/pipeline/SGI20141112_xsq2mut/*/*recal.bam'), projectN='somatic_mutation_single', clean=False, pbs=True, server='smc2', genome='hg19')
#	single(inputFilePathL=glob('/EQL7/pipeline/SGI20141126_xsq2mut/*/*recal.bam'), projectN='somatic_mutation_single', clean=False, pbs=True, server='smc2', genome='hg19')
#	single(inputFilePathL=glob('/EQL7/pipeline/SGI20141202_xsq2mut/*/*recal.bam'), projectN='somatic_mutation_single', clean=False, pbs=True, server='smc2', genome='hg19')
#	single(inputFilePathL=glob('/EQL7/pipeline/SGI20141210_xsq2mut/*/*recal.bam'), projectN='somatic_mutation_single', clean=False, pbs=True, server='smc2', genome='hg19')
#	single(inputFilePathL=glob('/EQL7/pipeline/SGI20141218_xsq2mut/*/*recal.bam'), projectN='somatic_mutation_single', clean=False, pbs=True, server='smc1', genome='hg19')
#	single(inputFilePathL=glob('/EQL7/pipeline/SGI20150112_xsq2mut/*/NS05_188_T*recal.bam'), projectN='somatic_mutation_single', clean=False, pbs=True, server='smc1', genome='hg19')
#	single(inputFilePathL=glob('/EQL7/pipeline/SGI20150121_xsq2mut/*/*recal.bam'), projectN='somatic_mutation_single', clean=False, pbs=True, server='smc1', genome='hg19')
#	single(inputFilePathL=glob('/EQL1/pipeline/SGI20150128_xsq2mut/*/IRCR_GBM14_599_T*recal.bam'), projectN='somatic_mutation_single', clean=False, pbs=True, server='smc1', genome='hg19')

#	tcga(tumorDirN='/EQL9/TCGA_WXS/TCGA_T', bloodDirN='/EQL10/TCGA_WXS/TCGA_B', projectN='TCGA_somatic', pbs=True, server='smc2', genome='hg19')

#	main(trioFileN='/home/ihlee/JK1/NGS/pipeline/PC_NS14_001TL_info.txt', projectN='somatic_mutation', tidL=['1'], clean=False, pbs=True, server='smc2', genome='hg19')
#	idL=[str(x) for x in range(1,58)]
#	idL=['54']
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='somatic_mutation', tidL=idL, clean=False, pbs=True, server='smc1', genome='hg19')
