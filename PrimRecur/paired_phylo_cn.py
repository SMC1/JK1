#!/usr/bin/python

import sys, os, random, re
from glob import glob
import mymysql
import DEG_annot

ABS_THR = 0.7 ## threshold for log2 ratio

def read_prim(inFileN, samp_id):
	inFile = open(inFileN, 'r')
	outH = {}
	for line in inFile:
		colL = line.rstrip().split('\t')
		sId = colL[0]
		gene = colL[1]
		cn_ratio = float(colL[2])
		call = 'KEEP'
		if abs(cn_ratio) < ABS_THR:
			call = 'REJECT'
		status = {samp_id: call, samp_id+'_val': cn_ratio}
		outH[gene] = status
	inFile.close()
	return outH

def add_recur(tabH, inFileN, samp_id):
	inFile = open(inFileN, 'r')
	for line in inFile:
		colL = line.rstrip().split('\t')
		sId = colL[0]
		gene = colL[1]
		cn_ratio = float(colL[2])
		call = 'KEEP'
		if abs(cn_ratio) < ABS_THR:
			call = 'REJECT'
		tabH[gene][samp_id] = call
		tabH[gene][samp_id+'_val'] = cn_ratio
	inFile.close()

def print_infile(datH, pid, ridL):
	outFile = open('infile', 'w')
	locFile = open('infile.loc', 'w')
	locFile.write('gene_symL\t%s\t%s_val' % (pid, pid))
	for i in range(len(ridL)):
		locFile.write('\t%s\t%s_val' % (ridL[i], ridL[i]))
	locFile.write('\n')
	cnt = 0
	for gene in datH:
		if 'KEEP' in datH[gene].values(): ## one of member has CNA in this gene
			locFile.write('%s' % (gene))
			locFile.write('\t%s\t%s' % (datH[gene][pid], datH[gene][pid+'_val']))
			for i in range(len(ridL)):
				locFile.write('\t%s\t%s' % (datH[gene][ridL[i]], datH[gene][ridL[i]+'_val']))
			locFile.write('\n')
			cnt += 1
	locFile.flush()
	locFile.close()
	
	outFile.write(' %s %s\n' % (len(ridL) + 2, cnt))

	outFile.write('Blood     ')
	for i in range(cnt):
		outFile.write('0')
	outFile.write('\n')

	outFile.write(pid + 'P')
	for i in range(9 - len(pid)):
		outFile.write(' ')
	for gene in datH:
		if 'KEEP' in datH[gene].values():
			if datH[gene][pid] == 'REJECT':
				outFile.write('0')
			else:
				outFile.write('1')
	outFile.write('\n')

	for rid in ridL:
		outFile.write(rid + 'R')
		for i in range(9 - len(rid)):
			outFile.write(' ')
		for gene in datH:
			if 'KEEP' in datH[gene].values():
				if datH[gene][rid] == 'REJECT':
					outFile.write('0')
				else:
					outFile.write('1')
		outFile.write('\n')

def parse_phylip(inFileN, locFileN, outFileN):
	inFile = open(inFileN, 'r')

	while True:
		line = inFile.readline()
		if 'means same as in the node below it on tree' in line:
			break
	inFile.readline()

	dataH = {}
	while True:
		line = inFile.readline()
		if line == '':
			break
	
		first = True
		while len(line.rstrip()) > 0:
			colL = filter(lambda x: len(x)>0, line.rstrip().split(' '))
			if first:
				key = 'consensus'
				data = ''.join(colL[1:])
			else:
				key = '-'.join(colL[:2])
				data = ''.join(colL[3:])
			if key not in dataH:
				dataH[key] = data
			else:
				dataH[key] += data
			line = inFile.readline()
			first = False

	locFile = open(locFileN, 'r')
	outFile = open(outFileN, 'w')
	locHead = locFile.readline().rstrip()
	colL = locHead.split('\t')
	idxH = {}
	for i in range(len(colL)):
		idxH[colL[i]] = i

	outFile.write('%s\tType\n' % locHead)
	cnt = 0
	for line in locFile:
		colL = line.rstrip().split('\t')
		if 'ND' in colL[1:]:
			outFile.write('%s\tUnused' % line.rstrip())
			outFile.write('\n')
		elif dataH['consensus'][cnt] == '1':
			outFile.write('%s\tCommon' % line.rstrip())
			outFile.write('\n')
			cnt += 1
		elif dataH['consensus'][cnt] == '?':
			outFile.write('%s\tConflict' % line.rstrip())
			outFile.write('\n')
			cnt += 1
		else:
			for key in dataH.keys():
				if key == 'consensus':
					continue
				if dataH[key][cnt] == '1':
					outFile.write('%s\t%s' % (line.rstrip(), key))
					outFile.write('\n')
					break
			cnt += 1
	outFile.flush()
	outFile.close()

def load_annot(inFileN='/EQL3/pipeline/somatic_mutect/signif_mutation.txt'):
	inFile = open(inFileN, 'r')
	colL = inFile.readline().rstrip().split('\t')
	idxH = {}
	for i in range(len(colL)):
		idxH[colL[i]] = i
	
	annotH = {}
	for line in inFile:
		colL = line.rstrip().split('\t')
		rm = re.match('(chr[^:]*):([0-9]*)~([0-9]*)', colL[idxH['locus']])
		(chr,chrSta,chrEnd) = rm.groups()
		ref = colL[idxH['ref']]
		alt = colL[idxH['alt']]
		if (chr,chrSta,chrEnd,ref,alt) not in annotH:
			annotH[(chr,chrSta,chrEnd,ref,alt)] = {}
			for col in ['gene_symL','ch_dna','ch_aa','ch_type','cosmic','mutsig']:
				annotH[(chr,chrSta,chrEnd,ref,alt)][col] = colL[idxH[col]]
	return annotH

### until it is merged into pipeline
import mybasic
mybasic.add_module_path(['NGS/pipeline'])
import mypipe
trioH = mypipe.read_trio(bamDirL=mysetting.wxsBamDirL)
pairH = {}
for tid in trioH:
	if trioH[tid]['recur_id'] != []:
		pid = trioH[tid]['prim_id'][0][:-5]
		pairH[pid] = map(lambda x: x[:-5], trioH[tid]['recur_id'])
####
#(con,cursor) = mymysql.connectDB(db='ircr1')
#tag = 'pair_R:%'
#cursor.execute('select distinct samp_id from sample_tag where tag like "%s"' % tag)
#sIdL_p = [x for (x,) in cursor.fetchall()]
#
#tag = 'XSeq%%,N'
#cursor.execute('select distinct samp_id from sample_tag where tag like "%s"' % tag)
#wxsL = [x for (x,) in cursor.fetchall()]
#
#pairH = {}
#for sId_p in sIdL_p:
#	if sId_p not in wxsL:
#		continue
#	if sId_p in ['S8A']: # no paired sample, yet
#		continue
#	tag = 'pair_P:%s' % sId_p
#	cursor.execute('select distinct samp_id from sample_tag where tag = "%s"' % tag)
#	sIdL_r = [x for (x,) in cursor.fetchall()]
#	for sId_r in sIdL_r:
#		if sId_r not in wxsL:
#			continue
#		if sId_p not in pairH:
#			pairH[sId_p] = []
#		pairH[sId_p].append(sId_r)
#print pairH
#sys.exit(0)
####
cnaDirRoot = '/EQL3/pipeline/CNA'
outDir = '/EQL1/PrimRecur/phylogeny_cna_0.7'
if not os.path.isdir(outDir):
	os.system('mkdir %s' % outDir)
for pid in pairH:
	if pid not in ['S567']:
		continue
	os.system('cp ~/phylip-3.695/exe/font1 fontfile')
	inFileN = glob('%s/*/%s*.cn_gene.dat' % (cnaDirRoot, pid))
	if len(inFileN) > 0:
		datH = read_prim(inFileN[0], pid)
	for rid in pairH[pid]:
		inFileN = glob('%s/*/%s*.cn_gene.dat' % (cnaDirRoot, rid))
		if len(inFileN) > 0:
			add_recur(datH, inFileN[0], rid)
	print_infile(datH, pid, pairH[pid])
	infile = '%s.CNA.pars_infile' % (pid)
	locfile = '%s.CNA.pars_locfile' % (pid)
	loutfile = '%s.CNA.pars_locfile.out' % (pid)
	lout_annotFile = '%s.CNA.pars_locfile_annot.txt' % (pid)
	tree = '%s.CNA.pars_intree' % (pid)
	outfile = '%s.CNA.pars_outfile' % (pid)

	cmd = '(echo -e "5\nY" | ~/phylip-3.695/exe/pars); mv outtree intree; cp intree %s; mv outfile %s; mv infile %s; mv infile.loc %s' % (tree, outfile, infile, locfile)
	os.system(cmd)
	psfile = '%s.CNA.pars_tree.ps' % (pid)
	cmd = '(echo "Y" | ~/phylip-3.695/exe/drawtree); mv plotfile %s; rm -f intree' % (psfile)
	os.system(cmd)
	os.system('rm -f fontfile')
	parse_phylip(outfile, locfile, loutfile)
	DEG_annot.gene_annot(loutfile, lout_annotFile)
	os.system('mv %s.CNA.pars_* %s' % (pid, outDir))
