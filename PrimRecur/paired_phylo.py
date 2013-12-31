#!/usr/bin/python

import sys, os, random, re
import mymysql
#contig	position	context	ref_allele	alt_allele	tumor_name	normal_name	score	dbsnp_site	covered	power	tumor_power	normal_power	total_pairs	improper_pairs	map_Q0_reads	t_lod_fstar	tumor_f	contaminant_fraction	contaminant_lod	t_ref_count	t_alt_count	t_ref_sum	t_alt_sum	t_ref_max_mapq	t_alt_max_mapq	t_ins_count	t_del_count	normal_best_gt	init_n_lod	n_ref_count	n_alt_count	n_ref_sum	n_alt_sum	judgement

MIN_COV = 20
MIN_FRAC = 0.05

def read_mutect(inFileN, samp_id):
	inFile = open(inFileN, 'r')
	inFile.readline()
	header = inFile.readline().rstrip()
	cols = header.split('\t')
	idxH = {}
	for i in range(len(cols)):
		idxH[cols[i]] = i
	
	outH = {}
	for line in inFile:
		colL = line.rstrip().split('\t')

		chr = colL[idxH['contig']]
		pos = colL[idxH['position']]
		ref = colL[idxH['ref_allele']]
		alt = colL[idxH['alt_allele']]
		status = {samp_id: colL[idxH['judgement']], samp_id+'_ref': colL[idxH['t_ref_count']], samp_id+'_alt': colL[idxH['t_alt_count']], 'n_ref': colL[idxH['n_ref_count']], 'n_alt': colL[idxH['n_alt_count']]}
		cov = int(colL[idxH['t_alt_count']]) + int(colL[idxH['t_ref_count']])
		ncov = int(colL[idxH['n_alt_count']]) + int(colL[idxH['n_ref_count']])
		frac = 0.0
		if cov > 0:
			frac = float(colL[idxH['t_alt_count']]) / float(cov)
		if colL[idxH['judgement']] == 'KEEP' and (cov < MIN_COV or frac < MIN_FRAC or ncov < MIN_COV):
			status[samp_id] = 'REJECT'
		outH[(chr,pos,ref,alt)] = status
	inFile.close()
	return outH

def add_mutect(tabH, inFileN, samp_id):
	inFile = open(inFileN, 'r')
	inFile.readline()
	header = inFile.readline().rstrip()
	cols = header.split('\t')
	idxH = {}
	for i in range(len(cols)):
		idxH[cols[i]] = i

	for line in inFile:
		colL = line.rstrip().split('\t')

		chr = colL[idxH['contig']]
		pos = colL[idxH['position']]
		ref = colL[idxH['ref_allele']]
		alt = colL[idxH['alt_allele']]
		if (chr, pos, ref, alt) in tabH:
			tabH[(chr,pos,ref,alt)][samp_id] = colL[idxH['judgement']]
			tabH[(chr,pos,ref,alt)][samp_id+'_ref'] = colL[idxH['t_ref_count']]
			tabH[(chr,pos,ref,alt)][samp_id+'_alt'] = colL[idxH['t_alt_count']]
		else:
			print 'missing locus!'
			sys.exit(1)
		cov = int(colL[idxH['t_alt_count']]) + int(colL[idxH['t_ref_count']])
		frac = 0.0
		if cov > 0:
			frac = float(colL[idxH['t_alt_count']]) / float(cov)
		if colL[idxH['judgement']] == 'KEEP' and (cov < MIN_COV or frac < MIN_FRAC):
			tabH[(chr,pos,ref,alt)][samp_id] = 'REJECT'
	inFile.close()

def print_infile(datH, pid, ridL):
	outFile = open('infile', 'w')
	locFile = open('infile.loc', 'w')
	locFile.write('chrom\tpos\tref\talt\tn_ref\tn_alt\t%s\t%s_ref\t%s_alt' % (pid, pid, pid))
	for i in range(len(ridL)):
		locFile.write('\t%s\t%s_ref\t%s_alt' % (ridL[i], ridL[i], ridL[i]))
	locFile.write('\n')
	cnt = 0
	for var in datH:
		(chr,pos,ref,alt) = var
		if 'KEEP' not in datH[var].values():
			continue
		else:
			locFile.write('%s\t%s\t%s\t%s\t%s\t%s' % (chr, pos, ref, alt, datH[var]['n_ref'], datH[var]['n_alt']))
			locFile.write('\t%s\t%s\t%s' % (datH[var][pid], datH[var][pid+'_ref'], datH[var][pid+'_alt']))
			for i in range(len(ridL)):
				locFile.write('\t%s\t%s\t%s' % (datH[var][ridL[i]], datH[var][ridL[i]+'_ref'], datH[var][ridL[i]+'_alt']))
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
	for var in datH:
		if 'KEEP' not in datH[var].values():
			continue
		else:
			if datH[var][pid] == 'REJECT':
				outFile.write('0')
			else:
				outFile.write('1')
	outFile.write('\n')

	for rid in ridL:
		outFile.write(rid + 'R')
		for i in range(9 - len(rid)):
			outFile.write(' ')
		for var in datH:
			(chr,pos,ref,alt) = var
			if 'KEEP' not in datH[var].values():
				continue
			else:
				if datH[var][rid] == 'REJECT':
					outFile.write('0')
				else:
					outFile.write('1')
		outFile.write('\n')

def parse_phylip(inFileN, locFileN, outFileN, annotH):
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

	outFile.write('%s\tType\tgene_sym\tch_dna\tch_aa\tch_type\tcosmic\tmutsig\n' % locHead)
	cnt = 0
	for line in locFile:
		colL = line.rstrip().split('\t')
		var = (colL[0], colL[1], colL[1], colL[2], colL[3])
		if dataH['consensus'][cnt] == '1':
			outFile.write('%s\tCommon' % line.rstrip())
			for c in ['gene_symL','ch_dna','ch_aa','ch_type','cosmic','mutsig']:
				outFile.write('\t%s' % annotH[var][c])
			outFile.write('\n')
		elif dataH['consensus'][cnt] == '?':
			outFile.write('%s\tConflict' % line.rstrip())
			for c in ['gene_symL','ch_dna','ch_aa','ch_type','cosmic','mutsig']:
				outFile.write('\t%s' % annotH[var][c])
			outFile.write('\n')
		else:
			for key in dataH.keys():
				if key == 'consensus':
					continue
				if dataH[key][cnt] == '1':
					outFile.write('%s\t%s' % (line.rstrip(), key))
					for c in ['gene_symL','ch_dna','ch_aa','ch_type','cosmic','mutsig']:
						outFile.write('\t%s' % annotH[var][c])
					outFile.write('\n')
					break
		cnt += 1
	outFile.flush()
	outFile.close()

def load_annot(inFileN='/EQL3/pipeline/somatic_mutect/signif_mutation_normal.txt'):
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

(con,cursor) = mymysql.connectDB(db='ircr1')
tag = 'pair_R:%'
cursor.execute('select distinct samp_id from sample_tag where tag like "%s"' % tag)
sIdL_p = [x for (x,) in cursor.fetchall()]

tag = 'XSeq%%,N'
cursor.execute('select distinct samp_id from sample_tag where tag like "%s"' % tag)
wxsL = [x for (x,) in cursor.fetchall()]

pairH = {}
for sId_p in sIdL_p:
	if sId_p not in wxsL:
		continue
	if sId_p in ['S8A']: # no paired sample, yet
		continue
	tag = 'pair_P:%s' % sId_p
	cursor.execute('select distinct samp_id from sample_tag where tag = "%s"' % tag)
	sIdL_r = [x for (x,) in cursor.fetchall()]
	for sId_r in sIdL_r:
		if sId_r not in wxsL:
			continue
		if sId_p not in pairH:
			pairH[sId_p] = []
		pairH[sId_p].append(sId_r)

inDir = '/EQL3/pipeline/somatic_mutect/'
annotH = load_annot()
for pid in pairH:
	os.system('cp ~/phylip-3.695/exe/font1 fontfile')
	inFileN = inDir + '%sT.union_pos.mutect' % pid[1:]
	datH = read_mutect(inFileN, pid)
	for rid in pairH[pid]:
		inFileN = inDir + '%sT.union_pos.mutect' % rid[1:]
		add_mutect(datH, inFileN, rid)
	
	print_infile(datH, pid, pairH[pid])
	infile = '%s%s.pars_infile' % (inDir, pid)
	locfile = '%s%s.pars_locfile' % (inDir, pid)
	loutfile = '%s%s.pars_locfile.out' % (inDir, pid)
	tree = '%s%s.pars_intree' % (inDir, pid)
	outfile = '%s%s.pars_outfile' % (inDir, pid)

	#odd = random.randint(1,100) * 2 - 1
	#ttt = random.randint(1,1000)
	cmd = '(echo -e "5\nY" | ~/phylip-3.695/exe/pars); mv outtree intree; cp intree %s; mv outfile %s; mv infile %s; mv infile.loc %s' % (tree, outfile, infile, locfile)
	os.system(cmd)
	psfile = '%s/%s.tree.ps' % (inDir, pid)
	cmd = '(echo "Y" | ~/phylip-3.695/exe/drawtree); mv plotfile %s; rm -f intree' % (psfile)
	os.system(cmd)
	os.system('rm -f fontfile')
	parse_phylip(outfile, locfile, loutfile, annotH)
