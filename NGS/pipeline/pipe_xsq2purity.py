#!/usr/bin/python

import sys, os, re
import mysetting, mypipe
from glob import glob

## SYSTEM CONFIGURATION

from mypipe import storageBase
from mypipe import apacheBase

def main(trioFileN, projectN, clean=False, pbs=False, server='smc1', genome='hg19', sampL=[]):
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

#		if tid not in ['43']:
#			continue

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
			sys.stderr.write('Can\'t find .mutscan\n')
			sys.exit(1)

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
				cnN = os.popen('find /EQL3/pipeline/CNA -name %s*.ngCGH.seg' % sampN).readlines()[0].rstrip()

				cmd = '/usr/bin/python ~/JK1/NGS/pipeline/pipe_s_xsq2purity.py -i \'%s\' -j %s -k %s -n %s -p %s -c %s -s %s -g %s' % (procN, mutscanN, cnN, sampN, projectN, clean, server, genome)
				print sampN
				print procN, mutscanN, cnN
				if pbs:
					log = '%s/%s.Xsq2purity.qlog' % (storageBase+projectN+'/'+sampN,sampN)
					os.system('echo "%s" | qsub -N x2purity_%s -o %s -j oe' % (cmd, sampN, log))
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
					cnN = os.popen('find /EQL3/pipeline/CNA -name %s*.ngCGH.seg' % sampN).readlines()[0].rstrip()

					cmd = '/usr/bin/python ~/JK1/NGS/pipeline/pipe_s_xsq2purity.py -i \'%s\' -j %s -k %s -n %s -p %s -c %s -s %s -g %s' % (procN, mutscanN, cnN, sampN, projectN, clean, server, genome)
					print sampN
					print procN, mutscanN, cnN
					if pbs:
						log = '%s/%s.Xsq2purity.qlog' % (storageBase+projectN+'/'+sampN,sampN)
						os.system('echo "%s" | qsub -N x2purity_%s -o %s -j oe' % (cmd, sampN, log))
					else:
						log = '%s/%s.Xsq2purity.qlog' % (storageBase+projectN, sampN)
						os.system('(%s) 2> %s' % (cmd, log))
			##for each recur
		## recur of pair


if __name__ == '__main__':
#	sampNL = ['S050_T_SS','S179_T_SS','S223_T_SS','S302_T_SS','S320_T_SS','S334_T_SS','S335_T_SS','S388_T_SS','S3A_T_SS','S464_T_SS','S470_T_SS','S520_T_SS','S567_T_SS','S585_T_SS','S732_T_SS','S768_T_SS']
#	sampNL = ['S015_T_SS','S092_T_SS','S10A_T_SS','S10B_T_SS','S11A_T_SS','S11B_T_SS','S12A_T_SS','S12B_T_SS','S14A_T_SS','S14B_T_SS','S202_T_SS','S240_T_SS','S243_T_SS','S323_T_SS','S386_T_SS','S3B_T_SS','S421_T_SS','S5A_T_SS','S5B_T_SS','S722_T_SS','S723_T_SS','S796_T_SS','S7A_T_SS','S7B_T_SS','S8A_T_SS','S8B_T_SS','S9A_T_SS','S9B_T_SS']
	sampNL = []
	main(trioFileN = '/EQL1/NSL/clinical/trio_info.txt', projectN='Purity', clean=False, pbs=True, server='smc1', genome='hg19',sampL=sampNL)
