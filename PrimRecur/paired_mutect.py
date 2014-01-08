#!/usr/bin/python

import sys, os, re

## mutect_trio_info.txt (tab-delimited txt)
## column 1: trio #
## column 2: role in trio ('Normal', 'Primary', 'Recurrent')
## column 3: sample #
## column 4: bam file name or standardized sample prefix

trioF = open('mutect_trio_info.txt', 'r')
#bamDirL = ['/EQL1/NSL/WXS/exome_20130529/','/EQL1/NSL/exome_bam/','/EQL1/pipeline/ExomeSeq_20130723/','/EQL3/pipeline/SGI20131031_xsq2mut/','/EQL3/pipeline/SGI20131119_xsq2mut/']
bamDirL = ['/EQL3/pipeline/somatic_mutect/','/EQL3/pipeline/SGI20131212_xsq2mut/','/EQL3/pipeline/SGI20131119_xsq2mut/', '/EQL3/pipeline/SGI20131216_xsq2mut/']

trioH = {}
for line in trioF:
	if line[0] == '#':
		continue
	cols = line.rstrip().split('\t')
	tid = cols[0]
	role = cols[1]
	sid = cols[2]
	if len(cols) > 3:
		prefix = cols[3]
	else:
		if role == 'Normal':
			prefix = 'S'+sid+'_B_SS'
		else:
			prefix = 'S'+sid+'_T_SS'
	sampFileNL = []
	for bamDir in bamDirL:
		sampFileNL += os.popen('find %s -name %s*recal.bam' % (bamDir, prefix)).readlines()
#		sampFileNL += os.popen('find %s -name *%s*recal.bam' % (bamDir, sid)).readlines()
	if tid not in trioH:
		trioH[tid] = {'prim_id':[], 'recur_id':[], 'Normal':[], 'Primary':[], 'Recurrent':[]}
		if role == 'Primary':
			trioH[tid]['prim_id'].append(prefix)
		elif role == 'Recurrent':
			trioH[tid]['recur_id'].append(prefix)
		if len(sampFileNL) > 0:
			trioH[tid][role].append(sampFileNL[0].rstrip())
	else:
		if role == 'Primary':
			trioH[tid]['prim_id'].append(prefix)
		elif role == 'Recurrent':
			trioH[tid]['recur_id'].append(prefix)
		if len(sampFileNL) > 0:
			trioH[tid][role].append(sampFileNL[0].rstrip())

#for tid in sorted(trioH.keys()):
#	if tid not in ['25','26','27','28','29','30','31','32']:
#		continue
#	print tid, trioH[tid]['prim_id'], trioH[tid]['recur_id']
#	for role in ['Normal','Primary','Recurrent']:
#		print role,trioH[tid][role]
#sys.exit(1)


outDir='/EQL3/pipeline/somatic_mutect'
outDir='/EQL6/pipeline/somatic_mutect'

## assume 1 primary & normal per trio
for tid in trioH:
#	if tid not in ['25','26','27','28','29','30','31','32']:
#		continue
	if trioH[tid]['prim_id'] != []:
		sampN = trioH[tid]['prim_id'][0]
		tumor = trioH[tid]['Primary'][0]
		normal = trioH[tid]['Normal'][0]
		cmd = 'python ~/JK1/NGS/mutation/mutect_pair.py -t %s -n %s -o %s -s %s -m 25g -g hg19 -p %s' % (tumor, normal, outDir, sampN, False)
#		print cmd
		os.system(cmd)
	
	if trioH[tid]['recur_id'] != []:
		for recur in range(len(trioH[tid]['Recurrent'])):
			sampN = trioH[tid]['recur_id'][recur]
			tumor = trioH[tid]['Recurrent'][recur]
			normal = trioH[tid]['Normal'][0]
			cmd = 'python ~/JK1/NGS/mutation/mutect_pair.py -t %s -n %s -o %s -s %s -m 25g -g hg19 -p %s' % (tumor, normal, outDir, sampN, False)
#			print cmd
			os.system(cmd)
