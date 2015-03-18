#!/usr/bin/python

import sys, os, re
import mysetting, mypipe, mysetting
from glob import glob

## SYSTEM CONFIGURATION

def main(trioFileN, projectN, clean=False, pbs=False, server='smc1', genome='hg19', sampL=[]):
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
		## must have normal sample
		if trioH[tid]['norm_id'] == []:
			continue

		norm_id = trioH[tid]['norm_id'][0]
#		if norm_id == 'S567_B_SS': ## id flip for mutscan(B)
#			norm_id = 'S567_T_SS'
		mutscanN = ''
		for dir in mysetting.wxsMutscanDirL:
			mutscanL = os.popen('find %s -name %s*.mutscan' % (dir, norm_id)).readlines()
			if len(mutscanL) > 0:
				mutscanN = mutscanL[0].rstrip()
				break
		if mutscanN == '': ## .mutscan not found
			print norm_id
			sys.stderr.write('Can\'t find .mutscan\n')
#			sys.exit(1)
			continue

		if trioH[tid]['prim_id'] != []:
			sampN = trioH[tid]['prim_id'][0]
			if sampL == [] or (sampL != [] and sampN in sampL):
				procN = ''
				for dir in mysetting.wxsPileupProcDirL:
					id = sampN
#					if sampN == 'S567_T_SS': ## id flip for pileup_proc
#						id = 'S567_B_SS'
					fileL = os.popen('find %s -name %s*chr*.pileup_proc' % (dir, id)).readlines()
					if len(fileL) > 0:
						procDir = list(set(map(lambda x: os.path.dirname(x.rstrip()), fileL)))[0]
						procN = '%s/%s*chr*.pileup_proc' % (procDir,id)
						break
				if procN == '': ## .pileup_proc not found
					sys.stderr.write('Can\'t find .pileup_proc\n')
					sys.exit(1)
				cnN = os.popen('find %s -name %s*.ngCGH.seg' % (mysetting.wxsCNADir,sampN)).readlines()[0].rstrip()

				cmd = '/usr/bin/python %s/NGS/pipeline/pipe_s_xsq2purity.py -i \'%s\' -j %s -k %s -n %s -p %s -c %s -s %s -g %s' % (mysetting.SRC_HOME, procN, mutscanN, cnN, sampN, projectN, clean, server, genome)
				print sampN
				print procN, mutscanN, cnN
				if pbs:
					log = '%s/%s.Xsq2purity.qlog' % (storageBase+projectN+'/'+sampN,sampN)
					os.system('echo "%s" | qsub -q %s -N x2purity_%s -o %s -j oe' % (cmd, server, sampN, log))
				else:
					log = '%s/%s.Xsq2purity.qlog' % (storageBase+projectN, sampN)
					os.system('(%s) 2> %s' % (cmd, log))
		## primary of pair
	
		if trioH[tid]['recur_id'] != []:
			for recur in range(len(trioH[tid]['Recurrent'])):
				sampN = trioH[tid]['recur_id'][recur]
				if sampL == [] or (sampL != [] and sampN in sampL):
					procN = ''
					for dir in mysetting.wxsPileupProcDirL:
						fileL = os.popen('find %s -name %s*chr*.pileup_proc' % (dir, sampN)).readlines()
						if len(fileL) > 0:
							procDir = list(set(map(lambda x: os.path.dirname(x.rstrip()), fileL)))[0]
							procN = '%s/%s*chr*.pileup_proc' % (procDir,sampN)
							break
					if procN == '': ## .pileup_proc not found
						sys.stderr.write('Can\'t find .pileup_proc\n')
						sys.exit(1)
					cnN = os.popen('find %s -name %s*.ngCGH.seg' % (mysetting.wxsCNADir,sampN)).readlines()[0].rstrip()

					cmd = '/usr/bin/python %s/NGS/pipeline/pipe_s_xsq2purity.py -i \'%s\' -j %s -k %s -n %s -p %s -c %s -s %s -g %s' % (mysetting.SRC_HOME, procN, mutscanN, cnN, sampN, projectN, clean, server, genome)
					print sampN
					print procN, mutscanN, cnN
					if pbs:
						log = '%s/%s.Xsq2purity.qlog' % (storageBase+projectN+'/'+sampN,sampN)
						os.system('echo "%s" | qsub -q %s -N x2purity_%s -o %s -j oe' % (cmd, server, sampN, log))
					else:
						log = '%s/%s.Xsq2purity.qlog' % (storageBase+projectN, sampN)
						os.system('(%s) 2> %s' % (cmd, log))
			##for each recur
		## recur of pair


if __name__ == '__main__':
#	sampNL = ['S050_T_SS','S179_T_SS','S223_T_SS','S302_T_SS','S320_T_SS','S334_T_SS','S335_T_SS','S388_T_SS','S3A_T_SS','S464_T_SS','S470_T_SS','S520_T_SS','S567_T_SS','S585_T_SS','S732_T_SS','S768_T_SS']
#	sampNL = ['S015_T_SS','S092_T_SS','S10A_T_SS','S10B_T_SS','S11A_T_SS','S11B_T_SS','S12A_T_SS','S12B_T_SS','S14A_T_SS','S14B_T_SS','S202_T_SS','S240_T_SS','S243_T_SS','S323_T_SS','S386_T_SS','S3B_T_SS','S421_T_SS','S5A_T_SS','S5B_T_SS','S722_T_SS','S723_T_SS','S796_T_SS','S7A_T_SS','S7B_T_SS','S8A_T_SS','S8B_T_SS','S9A_T_SS','S9B_T_SS']
#	sampNL = ['IRCR_GBM_363_TD_SS','IRCR_GBM_363_TM_SS', 'S317_2_T_SS']
#	sampNL = ['S317_T_SS','S317_2_T_SS','S316_T_SS']
#	sampNL = ['S189_T_SS','S189_2_T_SS']
#	sampNL = ['S210_T_SS']
#	sampNL = ['S364_T_SS']
#	sampNL = ['IRCR_GBM13_342_T_SS']
#	sampNL = ['IRCR_GBM14_458_T_SS','IRCR_GBM14_459_T01_SS','IRCR_GBM14_459_T02_SS']
#	sampNL = ['IRCR_GBM10_038_T_SS','IRCR_GBM12_199_T_SS']
#	sampNL = ['IRCR_GBM_352_TL_SS','IRCR_GBM_352_TR_SS']
#	sampNL = ['IRCR_GBM14_499_T02_SS']
#	sampNL = ['IRCR_GBM14_524_T_SS','IRCR_GBM14_526_T_SS','IRCR_GBM14_529_T_SS']
#	sampNL = ['IRCR_GBM14_527_T02_SS','IRCR_GBM14_531_T01_SS','IRCR_GBM14_533_T_SS','IRCR_GBM14_536_T_SS','IRCR_GBM14_541_T_SS','IRCR_GBM14_549_T01_SS','IRCR_GBM14_549_T02_SS','IRCR_GBM14_549_T03_SS']
#	sampNL = ['IRCR_GBM14_542_T01_SS']
#	sampNL = ['IRCR_GBM14_534_T_SS']
#	sampNL = ['IRCR_GBM14_366_T_SS','IRCR_GBM14_414_T_SS','IRCR_GBM13_300_T_SS','IRCR_GBM14_485_T_SS','IRCR_GBM14_494_T_SS','IRCR_GBM14_487_T_SS','IRCR_GBM14_503_T_SS','IRCR_GBM14_504_T03_SS','IRCR_GBM14_509_T_SS','IRCR_GBM14_510_T_SS','IRCR_GBM14_517_T_SS','IRCR_BMC14_061_T_SS','IRCR_MBT14_162_T_SS','IRCR_GBM14_500_T_SS','IRCR_GBM14_530_T_SS']
#	sampNL = ['IRCR_GBM14_366_T_SS','IRCR_GBM14_412_T_SS','IRCR_GBM14_472_T_SS','IRCR_GBM14_476_T03_SS','IRCR_GBM14_508_T_SS','IRCR_GBM14_511_T_SS','IRCR_BMC14_061_T_SS','IRCR_GBM13_292_T_SS','IRCR_GBM14_446_T_SS']
#	sampNL = ['IRCR_GBM14_559_T02_SS','IRCR_GBM14_567_T_SS']
#	sampNL = ['IRCR_GBM14_565_T_SS','IRCR_GBM14_559_T01_SS','IRCR_GBM14_570_T02_SS','IRCR_GBM14_574_T_SS','IRCR_GBM14_576_T_SS']
#	dirN = '/EQL7/pipeline/SGI20141021_xsq2mut/'
#	dirN = '/EQL7/pipeline/SGI20141027_xsq2mut/'
#	dirN = '/EQL7/pipeline/SGI20141103_xsq2mut/'
#	sampNL = filter(lambda x: os.path.isdir(dirN + x) and '_B_SS' not in x, os.listdir(dirN))
#	for sampN in ['IRCR_GBM14_606_T_SS']:
#		sampNL.remove(sampN)
#	sampNL = ['IRCR_GBM14_618_T_SS']
#	sampNL = ['IRCR_GBM14_607_T02_SS','IRCR_GBM11_067_T_SS','IRCR_GBM14_516_T_SS','IRCR_GBM14_593_T_SS','IRCR_GBM13_296_T_SS','IRCR_GBM14_566_T_SS']
#	sampNL = ['IRCR_GBM12_185_T_SS','IRCR_GBM12_190_T_SS','IRCR_GBM12_192_T_SS','IRCR_GBM11_131_T_SS','IRCR_GBM14_617_T_SS','IRCR_GBM14_619_T01_SS','IRCR_GBM14_619_T02_SS','IRCR_GBM14_626_T_SS','IRCR_GBM14_614_T_SS','IRCR_GBM14_616_T_SS','IRCR_GBM14_636_T_SS','IRCR_GBM13_231_T_SS','IRCR_GBM13_245_T_SS','IRCR_GBM14_639_T01_SS','IRCR_GBM14_639_T02_SS']
#	sampNL = ['IRCR_GBM14_629_T_SS']
#	sampNL = ['IRCR_GBM14_664_T01_SS'] #,'IRCR_GBM14_664_T02_SS','IRCR_GBM14_665_T01_SS','IRCR_GBM14_665_T02_SS']
#	sampNL = ['IRCR_GBM14_655_T_SS']
#	sampNL = ['IRCR_GBM13_352_T01_C01_SS','IRCR_GBM13_352_T02_C01_SS']
#	sampNL = ['IRCR_GBM12_165_T_SS','IRCR_GBM14_427_T_SS']
#	sampNL = ['IRCR_GBM14_393_T_SS']
#	sampNL = ['IRCR_GBM15_677_T_SS']
#	sampNL = ['IRCR_GBM15_682_T_SS']
#	sampNL = ['IRCR_GBM13_225_T_SS','IRCR_GBM10_002_T_SS','IRCR_GBM13_327_T_SS','IRCR_GBM14_390_T_SS','IRCR_GBM14_399_T_SS','IRCR_GBM14_505_T_SS','IRCR_GBM14_514_T_SS','IRCR_GBM14_632_T_SS','IRCR_GBM14_553_T_SS','IRCR_GBM14_570_T01_SS']
	sampNL = ['IRCR_GBM11_117_T_SS','IRCR_GBM14_410_T_SS','IRCR_GBM14_630_T_SS']
	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='Purity', clean=False, pbs=True, server='smc1', genome='hg19',sampL=sampNL)
#	main(trioFileN = '/EQL5/pipeline/Young_pair_info.txt', projectN='CRC_xsq2purity', clean=False, pbs=True, server='smc1', genome='hg19', sampL=[])

#	main(trioFileN='/home/ihlee/JK1/NGS/pipeline/PC_NS14_001TL_info.txt', projectN='Purity', clean=False, pbs=True, server='smc1', genome='hg19', sampL=[])
