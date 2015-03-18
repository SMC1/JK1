#!/usr/bin/python

import sys, os, re
import mysetting, mypipe, mybasic
from glob import glob

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
		if trioH[tid]['Normal'] == [] or trioH[tid]['prim_id'] == []:
			continue

		bamS = set()
		if trioH[tid]['prim_id'] != []: ##primary
			bamS.add(trioH[tid]['Normal'][0])
			bamS.add(trioH[tid]['Primary'][0])

		if trioH[tid]['recur_id'] != []: ##recurrent
			for recur in range(len(trioH[tid]['Recurrent'])):
				bamS.add(trioH[tid]['Recurrent'][recur])

		sampN = trioH[tid]['prim_id'][0]
		
		cmd = '/usr/bin/python %s/NGS/pipeline/pipe_s_xsq2phylotree.py -i %s -n %s -p %s -c %s -s %s -g %s' % (mysetting.SRC_HOME, ','.join(list(bamS)), sampN, projectN, False, server, genome)
		print cmd

		if pbs:
			log = '%s/%s.Xsq2phylotree.qlog' % (storageBase+projectN+'/'+sampN,sampN)
			os.system('echo "%s" | qsub -q %s -N x2phylotree_%s -o %s -j oe' % (cmd, server, sampN, log))
		else:
			log = '%s/%s.Xsq2phylotree.qlog' % (storageBase+projectN, sampN)
			os.system('(%s) 2> %s' % (cmd, log))

if __name__ == '__main__':
	#test
#	tidL = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','26','27','28','33','35','36','37','39','41','42','43','44','46','47','49','57','58','63','71','74','78','82','87']
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='Phylotree', tidL=tidL, clean=False, pbs=True, server='smc2', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='Phylotree', tidL=['71'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='Phylotree', tidL=['58'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='Phylotree', tidL=['37'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='Phylotree', tidL=['117','124'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='Phylotree', tidL=['87'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='Phylotree', tidL=['99'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='Phylotree', tidL=['125','126'], clean=False, pbs=True, server='smc1', genome='hg19')
#	main(trioFileN='/home/ihlee/JK1/NGS/pipeline/PC_NS14_001TL_info.txt', projectN='test', tidL=['1'], clean=False, pbs=True, server='smc1', genome='hg19')
	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='Phylotree', tidL=['37'], clean=False, pbs=True, server='smc1', genome='hg19')

## minimum allele fraction 0.2
	tidL = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','26','27','28','33','35','36','37','39','41','42','43','44','46','47','49','55','57','58','63','71','74','78','82','87','99','117','124']
#	tidL = ['125','126']
	tidL = ['6']
	tidL = ['37']
#	main(trioFileN='/EQL1/NSL/clinical/trio_info.txt', projectN='Phylotree_d20_f0.2', tidL=tidL, clean=False, pbs=True, server='smc1', genome='hg19')
