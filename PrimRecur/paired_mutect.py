#!/usr/bin/python

import sys, os, re

## mutect_trio_info.txt (tab-delimited txt)
## column 1: trio #
## column 2: role in trio ('Normal', 'Primary', 'Recurrent')
## column 3: sample #
## column 4: bam file name or standardized sample prefix

trioF = open('mutect_trio_info.txt', 'r')
bamDirL = ['/EQL1/NSL/WXS/exome_20130529/','/EQL1/NSL/exome_bam/','/EQL1/pipeline/ExomeSeq_20130723/']

trioH = {}
for line in trioF:
	cols = line.rstrip().split('\t')
	tid = cols[0]
	role = cols[1]
	sid = cols[2]
	prefix = cols[3]
	sampFileNL = []
	for bamDir in bamDirL:
		sampFileNL += os.popen('find %s -name %s*recal.bam' % (bamDir, prefix)).readlines()
		sampFileNL += os.popen('find %s -name *%s' % (bamDir, prefix)).readlines()
	if tid not in trioH:
		trioH[tid] = {}
		if role == 'Primary':
			trioH[tid]['prim_id'] = sid
		elif role == 'Recurrent':
			trioH[tid]['recur_id'] = sid
		if len(sampFileNL) > 0:
			trioH[tid][role] = sampFileNL[0].rstrip()
	else:
		if role == 'Primary':
			trioH[tid]['prim_id'] = sid
		elif role == 'Recurrent':
			trioH[tid]['recur_id'] = sid
		if len(sampFileNL) > 0:
			trioH[tid][role] = sampFileNL[0].rstrip()


for tid in trioH:
	outputN = trioH[tid]['Primary'].replace(".recal.bam","")
	sampN = outputN.split('/')[-1]
	if outputN.find('exome_bam') > 0:
		outputN = '/EQL1/NSL/exome_bam/mutation/%s' % sampN
	os.system('python /home/ihlee/JK1/NGS/mutation/mutect_pair.py -t %s -n %s -o %s -m 8g' % (trioH[tid]['Primary'], trioH[tid]['Normal'], outputN))

for tid in trioH:
	outputN = trioH[tid]['Recurrent'].replace(".recal.bam","")
	sampN = outputN.split('/')[-1]
	if outputN.find('exome_bam') > 0:
		outputN = '/EQL1/NSL/exome_bam/mutation/%s' % sampN
	os.system('python /home/ihlee/JK1/NGS/mutation/mutect_pair.py -t %s -n %s -o %s -m 8g' % (trioH[tid]['Recurrent'], trioH[tid]['Normal'], outputN))
