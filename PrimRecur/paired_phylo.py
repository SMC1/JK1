#!/usr/bin/python

import sys, os

ifile = open('/EQL1/PrimRecur/paired/somatic/8pair_mutect_union.dat', 'r')
outDir = '/EQL1/PrimRecur/paired/somatic'
idxH = {}
header = ifile.readline().rstrip()
cols = header.split('\t')
for i in range(len(cols)):
	idxH[cols[i]] = i

resH = {}
for line in ifile:
	arr = line.rstrip().split('\t')

	pair = arr[idxH['sId_pair']]
	var = '%s:%s:%s' % (arr[idxH['locus']], arr[idxH['ref']], arr[idxH['alt']])
	if pair not in resH:
		resH[pair] = {'common': [], 'p_only': [], 'r_only': [], 'annot': {'common': [], 'p_only': [], 'r_only': []}}
	p_stat = arr[idxH['p_status']]
	r_stat = arr[idxH['r_status']]
	if p_stat == 'REJECT' and r_stat != 'REJECT':
		## r only
		if var not in resH[pair]['r_only']:
			resH[pair]['r_only'].append(var)
		resH[pair]['annot']['r_only'].append(line.rstrip())
	elif p_stat != 'REJECT' and r_stat == 'REJECT':
		## p only
		if var not in resH[pair]['p_only']:
			resH[pair]['p_only'].append(var)
		resH[pair]['annot']['p_only'].append(line.rstrip())
	elif p_stat != 'REJECT' and r_stat != 'REJECT':
		## common
		if var not in resH[pair]['common']:
			resH[pair]['common'].append(var)
		resH[pair]['annot']['common'].append(line.rstrip())
ifile.close()

os.system('cp ~/phylip-3.695/exe/font1 fontfile')
for pair in resH:
	np = len(resH[pair]['p_only'])
	nr = len(resH[pair]['r_only'])
	nc = len(resH[pair]['common'])
	
	pId = pair.split('-')[0]
	rId = pair.split('-')[1]

	tree = '(Normal:0,(%sP:%s,%sR:%s):%s);' % (pId,np, rId,nr, nc)

	cmd = 'echo "%s" > intree' % tree
	cmd = '%s; cp ~/phylip-3.695/exe/font1 fontfile' % cmd
	cmd = '%s; (echo "Y" | ~/phylip-3.695/exe/drawtree); mv plotfile %s/%sT_%sT.paired_phylo.ps; rm -f intree fontfile' % (cmd, outDir, pId[1:], rId[1:])
	os.system(cmd)

	outPonly = open('%s/%sT_%sT.paired_phylo.Ponly' % (outDir, pId[1:], rId[1:]), 'w')
	outPonly.write('%s\n' % header)
	for line in resH[pair]['annot']['p_only']:
		outPonly.write('%s\n' % line)
	outPonly.flush()
	outPonly.close()
	outRonly = open('%s/%sT_%sT.paired_phylo.Ronly' % (outDir, pId[1:], rId[1:]), 'w')
	outRonly.write('%s\n' % header)
	for line in resH[pair]['annot']['r_only']:
		outRonly.write('%s\n' % line)
	outRonly.flush()
	outRonly.close()
	outCommon = open('%s/%sT_%sT.paired_phylo.common' % (outDir, pId[1:], rId[1:]), 'w')
	outCommon.write('%s\n' % header)
	for line in resH[pair]['annot']['common']:
		outCommon.write('%s\n' % line)
	outCommon.flush()
	outCommon.close()

