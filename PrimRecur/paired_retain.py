#!/usr/bin/python

import sys, itertools, random
import mymysql, mysetting

MIN_COV = 5 ## minimum total read depth
MIN_FRAC = 0.05 ## alternative allele fraction
MIN_MUTN = 5 # minimum alternative allele read count
MIN_MUTN_R = 2 ## minimum alternative allele read count in recur
MIN_FRAC_R = 0.02 ## alternative allele fraction in recur

cnd_mutH = {'has_norm':'(n_nReads_ref + n_nReads_alt) >= %d and (nReads_ref + nReads_alt) >= %d and nReads_alt >= %d and nReads_alt >= (nReads_alt+nReads_ref)*%s' % (MIN_COV, MIN_COV, MIN_MUTN, MIN_FRAC),'no_norm':'(nReads_ref + nReads_alt) >= %d and nReads_alt >= %d and nReads_alt >= (nReads_alt+nReads_ref)*%s' % (MIN_COV, MIN_MUTN, MIN_FRAC), 'has_rsq':'(r_nReads_ref + r_nReads_alt) >= %d and r_nReads_alt >= %d and r_nReads_alt >= (r_nReads_alt+r_nReads_ref)*%s' % (MIN_COV, MIN_MUTN, MIN_FRAC)}

cnd_mut_rH = {'mutation_normal':'(nReads_ref + nReads_alt) >= %d and nReads_alt >= %d and nReads_alt >= (nReads_alt+nReads_ref)*%s' % (MIN_COV, MIN_MUTN_R, MIN_FRAC_R),'mutation':'(nReads_ref + nReads_alt) >= %d and nReads_alt >= %d and nReads_alt >= (nReads_alt+nReads_ref)*%s' % (MIN_COV, MIN_MUTN_R, MIN_FRAC_R), 'mutation_rsq':'(r_nReads_ref + r_nReads_alt) >= %d and r_nReads_alt >= %d and r_nReads_alt >= (r_nReads_alt+r_nReads_ref)*%s' % (MIN_COV, MIN_MUTN_R, MIN_FRAC_R)}

def has_exome(samp_id, dbN='ircr1'):
	(con, cursor) = mymysql.connectDB(db=dbN)
	cursor.execute('select count(distinct samp_id) from sample_tag where (tag like "XSeq_TS%%" or tag like "XSeq_SS%%") and samp_id="%s"' % samp_id)
	idL = [x for (x,) in cursor.fetchall()]
	if int(idL[0]) > 0:
		return(True)
	else:
		return(False)

def has_normal(samp_id, dbN='ircr1'):
	(con, cursor) = mymysql.connectDB(db=dbN)
	cursor.execute('select count(distinct samp_id) from sample_tag where tag like "XSeq_%%,N" and samp_id = "%s"' % samp_id)
	idL = [x for (x,) in cursor.fetchall()]
	if int(idL[0]) > 0:
		return(True)
	else:
		return(False)

def has_rsq(samp_id, dbN='ircr1'):
	(con, cursor) = mymysql.connectDB(db=dbN)
	cursor.execute('select count(distinct samp_id) from sample_tag where tag="RNA-Seq" and samp_id="%s"' % samp_id)
	idL = [x for (x,) in cursor.fetchall()]
	if int(idL[0]) > 0:
		return(True)
	else:
		return(False)

def has_acgh(samp_id, dbN='ircr1'):
	(con, cursor) = mymysql.connectDB(db=dbN)
	cursor.execute('select count(distinct samp_id) from array_cn where samp_id="%s"' % samp_id)
	if cursor.fetchone()[0] > 0:
		return(True)
	else:
		return(False)

def random_combination(iterable, r):
	pool = tuple(iterable)
	n = len(pool)
	indices = sorted(random.sample(xrange(n), r))
	return tuple(pool[i] for i in indices)

def p_test(val, ret, van, fracH):
	cnt = 0
	all = set(fracH.keys())
	for i in range(5000):
		ret1 = set(random_combination(all, ret))
		van1 = set(random_combination(all-ret1, van))
		retSig = 1.0
		for p in ret1:
			retSig *= fracH[p]
		for p in van1:
			retSig /= (1-fracH[p])
		if retSig < val:
			cnt += 1
	## for i
	return(float(cnt)/5000.0)

def print_mutSig(datH, fracH):
	sys.stdout.write('gene\tretSig\tp-value\tCases retained\tCases vanished\n')
	for gene in datH:
		if gene == '':
			continue
		if len(datH[gene]['retain']) + len(datH[gene]['vanish']) > 1: ## shown in more than 2 pairs
			retSig = 1.0
			sys.stderr.write("%s <<<<<<\n" % gene)
			for p in datH[gene]['retain']:
				retSig *= fracH[p]
				sys.stderr.write("retained %s %s %s\n" % (p, fracH[p], retSig))
			for p in datH[gene]['vanish']:
				retSig /= (1-fracH[p])
				sys.stderr.write("vanished %s %s %s\n" % (p, fracH[p], retSig))
			ret = len(datH[gene]['retain'])
			van = len(datH[gene]['vanish'])
			sys.stderr.write('%s\t%s\t%s\tretained in %s/%s pairs\tvanished in %s/%s pairs\n' % (gene, retSig, p_test(retSig, ret, van, fracH), len(datH[gene]['retain']),datH[gene]['p_cnt'], len(datH[gene]['vanish']),datH[gene]['p_cnt']))
			sys.stdout.write('%s\t%s\t%s\tretained in %s/%s pairs\tvanished in %s/%s pairs\n' % (gene, retSig, p_test(retSig, ret, van, fracH), len(datH[gene]['retain']),datH[gene]['p_cnt'], len(datH[gene]['vanish']),datH[gene]['p_cnt']))

def retSig_CNA(mode='up', th=1.0, dbN='ircr1'):
	(con,cursor) = mymysql.connectDB(db=dbN)
	cursor.execute('select distinct samp_id from sample_tag where tag like "Pair_R:%%"')
	sidL = [x for (x,) in cursor.fetchall()]
	sidL.sort()

	geneH = {}
	fracH = {}
	for sid in sidL:
		if sid in ['S042']: ## consent form issue
			continue
		if '_X' in sid:
			continue
		cursor.execute('select distinct tag from sample_tag where tag like "Pair_R:%%" and samp_id="%s"' % sid)
		rid = cursor.fetchone()[0].split(':')[-1]

		pair = '%s:%s' % (sid, rid)

		if has_acgh(sid) and has_acgh(rid):
			tblN = 'array_cn'
		elif has_exome(sid) and has_exome(rid):
			tblN = 'xsq_cn'
		else:
			continue

		if mode == 'up':
			cursor.execute('select distinct gene_sym from %s where value_log2 >= %s and samp_id="%s"' % (tblN, th, sid))
			p_geneL = [item[0] for item in cursor.fetchall()]
			cursor.execute('select distinct gene_sym from %s where value_log2 >= %s and samp_id="%s"' % (tblN, th, rid))
			r_geneL = [item[0] for item in cursor.fetchall()]
		elif mode == 'dn':
			cursor.execute('select distinct gene_sym from %s where value_log2 <= %s and samp_id="%s"' % (tblN, th, sid))
			p_geneL = [item[0] for item in cursor.fetchall()]
			cursor.execute('select distinct gene_sym from %s where value_log2 <= %s and samp_id="%s"' % (tblN, th, rid))
			r_geneL = [item[0] for item in cursor.fetchall()]

		shared_geneL = list(set(p_geneL) & set(r_geneL))
		if len(p_geneL) < 1:
			continue
#		fracH[pair] = float(len(shared_geneL))/float(len(p_geneL))
		fracH[pair] = 0.5 ## uniform

		for gene in p_geneL:
			if gene in shared_geneL: ## retained
				if gene in geneH:
					geneH[gene]['retain'].append(pair)
					geneH[gene]['p_cnt'] += 1
				else:
					geneH[gene] = {'retain': [pair], 'vanish': [], 'p_cnt':1}
			else: ## vanished
				if gene in geneH:
					geneH[gene]['vanish'].append(pair)
					geneH[gene]['p_cnt'] += 1
				else:
					geneH[gene] = {'retain': [], 'vanish': [pair], 'p_cnt':1}
			##if
		##for
	print_mutSig(geneH, fracH)

def retSig_mut(useUniform=True, useUnmatched=False, dbN='ircr1'):
	(con,cursor) = mymysql.connectDB(db=dbN)
	cursor.execute('select distinct samp_id from sample_tag where tag like "Pair_R:%%"')
	sIdL = [x for (x,) in cursor.fetchall()]	
	sIdL.sort()

	cnd_eff = 'ch_type like "%%nonsense%%" or ch_type like "%%missense%%" or ch_type like "%%splice_acceptor%%" or ch_type like "%%splice_donor%%" or ch_type like "%%Nonstop%%" or ch_type like "%%stop_lost%%" or ch_type like "%%stop_gained%%"'

	fracH = {}
	geneH = {}
	for sid in sIdL:
		if sid in ['S042']: ## consent form issue
			continue
		if '_X' in sid:
			continue
		cursor.execute('select distinct tag from sample_tag where tag like "Pair_R:%%" and samp_id="%s"' % sid)
		rid = cursor.fetchone()[0].split(':')[-1]

		pair = '%s:%s' % (sid, rid)
		
		flag=''
		if has_exome(sid) and has_exome(rid):
			if has_normal(sid) and has_normal(rid):
				flag = 'has_norm'
				cnd_mut = cnd_mutH['has_norm']
			else:
				flag = 'no_norm'
				cnd_mut = cnd_mutH['no_norm']
		elif has_rsq(sid) and has_rsq(rid):
			flag = 'has_rsq'
			cnd_mut = cnd_mutH['has_rsq']
		else:
			continue

		if not useUnmatched and flag != 'has_norm':
			continue

		cursor.execute('select distinct concat(chrom,":",chrSta,":",chrEnd,":",ref,":",alt) from mutation_rxsq where (%s) and samp_id="%s"' % (cnd_mut, sid))
		p_mutL = [item[0] for item in cursor.fetchall()]

		stmt = 'select distinct concat(chrom,":",chrSta,":",chrEnd,":",ref,":",alt) from mutation where (%s) and samp_id="%s"' % (cnd_mut_rH['mutation'], rid)
		for t in ['mutation_normal','mutation_rsq']:
			stmt = '%s union select distinct concat(chrom,":",chrSta,":",chrEnd,":",ref,":",alt) from %s where (%s) and samp_id="%s"' % (stmt, t, cnd_mut_rH[t], rid)
		cursor.execute(stmt)
		r_mutL = [item[0] for item in cursor.fetchall()]

		if useUniform:
			fracH[pair] = 0.5
		else:
			if has_exome(sid) and has_normal(sid) and has_exome(rid) and has_normal(rid):
				comm = len(set(p_mutL) & set(r_mutL))
				fracH[pair] = float(comm) / float(len(p_mutL))
			else:
				fracH[pair] = 0.5

		cursor.execute('select distinct gene_symL from mutation_rxsq where (%s) and (%s) and samp_id="%s"' % (cnd_eff, cnd_mut, sid))
		tmpL = [item[0] for item in cursor.fetchall()]
		p_geneL = []
		for gene in tmpL:
			p_geneL += gene.split(',')
		p_geneL = list(set(p_geneL))

		for gene in p_geneL:
			cursor.execute('select distinct concat(chrom,":",chrSta,":",chrEnd,":",ref,":",alt) from mutation_rxsq where(%s) and (%s) and samp_id="%s" and gene_symL="%s"' % (cnd_eff, cnd_mut, sid, gene))
			m_pL = [item[0] for item in cursor.fetchall()]
			
			stmt = 'select distinct concat(chrom,":",chrSta,":",chrEnd,":",ref,":",alt) from mutation where (%s) and (%s) and samp_id="%s" and gene_symL="%s"' % (cnd_eff, cnd_mut_rH['mutation'], rid, gene)
			for t in ['mutation_normal','mutation_rsq']:
				stmt = '%s union select distinct concat(chrom,":",chrSta,":",chrEnd,":",ref,":",alt) from %s where (%s) and (%s) and samp_id="%s" and gene_symL="%s"' % (stmt, t, cnd_eff, cnd_mut_rH[t], rid, gene)
			cursor.execute(stmt)
			m_rL = [item[0] for item in cursor.fetchall()]

			retain = len(set(m_pL) & set(m_rL))
			if retain > 0: ## retained
				if gene in geneH:
					geneH[gene]['retain'].append(pair)
					geneH[gene]['p_cnt'] += 1
				else:
					geneH[gene] = {'retain': [pair], 'vanish':[], 'p_cnt':1}
			else: ## vanished
				if gene in geneH:
					geneH[gene]['vanish'].append(pair)
					geneH[gene]['p_cnt'] += 1
				else:
					geneH[gene] = {'retain': [], 'vanish':[pair], 'p_cnt':1}
		## for gene in p_geneL
	## for sid

	print_mutSig(geneH, fracH)

def paired_retain():
	retSig_mut(useUniform=False, useUnmatched=False)
#	retSig_CNA(mode='up', th=1.0)
#	retSig_CNA(mode='dn', th=-1.0)

if __name__ == '__main__':
	paired_retain()
