#!/usr/bin/python

import sys, os, re
import mysetting

homeDir = os.popen('echo $HOME','r').read().rstrip()
sys.path.append('%s/JK1/NGS/pipeline' % (homeDir))
import mypipe

bamDirL = mysetting.wxsBamDirL
trioH = mypipe.read_trio('/EQL1/NSL/clinical/trio_info.txt', bamDirL)

#for tid in sorted(trioH.keys()):
#	if tid not in ['41','42','46','47','48']:
#		continue
#	print tid, trioH[tid]['prim_id'], trioH[tid]['recur_id']
#	for role in ['Normal','Primary','Recurrent']:
#		print role,trioH[tid][role]
#sys.exit(1)

outDir='/EQL3/pipeline/somatic_mutect'

## assume 1 primary & normal per trio
for tid in trioH:
	if trioH[tid]['norm_id'] == []:
		continue
	if tid not in ['53']:
		continue

	norm = trioH[tid]['norm_id'][0]
	if trioH[tid]['prim_id'] != []:
		sampN = trioH[tid]['prim_id'][0]
		print norm,sampN
		tumor = trioH[tid]['Primary'][0]
		normal = trioH[tid]['Normal'][0]
		cmd = 'python ~/JK1/NGS/mutation/mutect_pair.py -t %s -n %s -o %s -s %s -m 25g -g hg19 -p %s' % (tumor, normal, outDir, sampN, True)
		os.system(cmd)
	
	if trioH[tid]['recur_id'] != []:
		for recur in range(len(trioH[tid]['Recurrent'])):
			sampN = trioH[tid]['recur_id'][recur]
			print norm,sampN
			tumor = trioH[tid]['Recurrent'][recur]
			normal = trioH[tid]['Normal'][0]
			cmd = 'python ~/JK1/NGS/mutation/mutect_pair.py -t %s -n %s -o %s -s %s -m 25g -g hg19 -p %s' % (tumor, normal, outDir, sampN, True)
			os.system(cmd)
