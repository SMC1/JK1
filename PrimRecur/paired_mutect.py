#!/usr/bin/python

import sys, os, re
import mysetting, mybasic

mybasic.add_module_path(['NGS/pipeline','NGS/mutation'])
import mutect_batch, somaticindeldetector_batch

import mypipe

bamDirL = mysetting.wxsBamDirL
trioH = mypipe.read_trio('/EQL1/NSL/clinical/trio_info.txt', bamDirL)

#for tid in sorted(trioH.keys()):
#	if tid not in ['59','60','61']:
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
	if tid not in ['63']:
		continue

	norm = trioH[tid]['norm_id'][0]
	if trioH[tid]['prim_id'] != []:
		sampN = trioH[tid]['prim_id'][0]
		print norm,sampN
		tumor = trioH[tid]['Primary'][0]
		normal = trioH[tid]['Normal'][0]
#		mutect_batch.mutect_pair(tBamN=tumor, nBamN=normal, outDirN=outDir, genome='hg19', server='smc1', pbs=False)
		somaticindeldetector_batch.paired_mode(tbam=tumor, nbam=normal, outDirN=outDir, sampN=sampN, pl='SS', genome='hg19', server='smc1', pbs=False)
	
	if trioH[tid]['recur_id'] != []:
		for recur in range(len(trioH[tid]['Recurrent'])):
			sampN = trioH[tid]['recur_id'][recur]
			print norm,sampN
			tumor = trioH[tid]['Recurrent'][recur]
			normal = trioH[tid]['Normal'][0]
#			mutect_batch.mutect_pair(tBamN=tumor, nBamN=normal, outDirN=outDir, genome='hg19', server='smc1', pbs=False)
			somaticindeldetector_batch.paired_mode(tbam=tumor, nbam=normal, outDirN=outDir, sampN=sampN, pl='SS', genome='hg19', server='smc1', pbs=False)
