#!/usr/bin/python

import sys, os, re
import mymysql


pileupDirL = ['/EQL1/NSL/WXS/exome_20130529/','/EQL1/NSL/exome_bam/mutation/pileup_proc/','/EQL1/pipeline/ExomeSeq_20130723/','/EQL3/pipeline/SGI20140103_xsq2mut/','/EQL3/pipeline/SGI20131119_xsq2mut/']

mutTypeH = { \
	'SKIP':('splice_skip_AF','delExons','nReads,nReads_w1','loc1','gene_sym'), \
	'3pDEL':('splice_eiJunc_AF','juncAlias','nReads,nReads_w','loc','gene_sym'), \
	'MUT':('mutation_normal','ch_aa','nReads_alt,nReads_ref','','gene_symL'), \
	'MUTR':('mutation_rsq','ch_aa','r_nReads_alt,r_nReads_ref','','gene_symL') \
	}


def lookupPileup(pileupDirL,sId,chrom,loc,ref,alt):

	inputFileNL = []
	
	for pileupDir in  pileupDirL:
		inputFileNL += os.popen('find %s -name %s_T_*%s.pileup_proc' % (pileupDir,sId,chrom)).readlines()

	if len(inputFileNL) > 1:
		inputFileNL = filter(lambda x: not re.match('.*KN.*', x),inputFileNL)

#	if len(set(inputFileNL)) != 1:
#		print 'Error:', list(set(inputFileNL))
#		raise Exception

	if len(inputFileNL) == 0:
		return None

	resultL = os.popen('grep -m 1 "^%s:%s," %s' % (chrom,loc,inputFileNL[0].rstrip()), 'r').readlines()

	if len(resultL)==0:
		return None
	else:
		tL = resultL[0].rstrip().split(',')
		if ref != tL[2]:
			raise Exception
		refCount = int(tL[3])
		altCount = tL[4].count(alt)
		return (altCount,refCount)


def main(outFileName):

	(con,cursor) = mymysql.connectDB(db='ircr1')

	resultL = []

	cursor.execute('select distinct samp_id from sample_tag where substring(tag,1,6)="pair_R" and samp_id!="S042" and \
		samp_id not like "%_X" and substring(samp_id,length(samp_id)-1)!="_2"')
	sIdL_prim = [x for (x,) in cursor.fetchall()]

	for (geneN,mutType,mutName) in mutL:

		for sId_p in sIdL_prim:

			(tbl,col,values,c_loc,c_gene_sym) = mutTypeH[mutType]

			cursor.execute('select t1.samp_id from sample_tag t1 where t1.tag="pair_P:%s" and \
				"%s" in (select t2.samp_id from sample_tag t2 where t2.tag=concat("pair_R:",t1.samp_id))' % (sId_p,sId_p))
			(sId_r,) = cursor.fetchone()

			cursor.execute('select %s from %s where %s="%s" and %s like "%%%s%%" and samp_id="%s"' % (values,tbl,c_gene_sym,geneN,col,mutName,sId_p))
			r_p = cursor.fetchone()

			cursor.execute('select %s from %s where %s="%s" and %s like "%%%s%%" and samp_id="%s"' % (values,tbl,c_gene_sym,geneN,col,mutName,sId_r))
			r_r = cursor.fetchone()

			if r_p or r_r:
			
				if mutType in ('SKIP','3pDEL'):
				
					cursor.execute('select distinct %s from %s where %s="%s" and %s="%s" and (samp_id="%s" or samp_id="%s")' % (c_loc,tbl,c_gene_sym,geneN,col,mutName,sId_p,sId_r))
					loc1 = cursor.fetchone()[0]

					if not r_p:
						cursor.execute('select nReads_w1 from splice_normal_loc1 where loc1="%s" and samp_id="%s"' % (loc1,sId_p))
						r_t = cursor.fetchone()
						if r_t:
							r_p = (0,r_t[0])

					if not r_r:
						cursor.execute('select nReads_w1 from splice_normal_loc1 where loc1="%s" and samp_id="%s"' % (loc1,sId_r))
						r_t = cursor.fetchone()
						if r_t:
							r_r = (0,r_t[0])

				elif mutType=='MUT':
					
					cursor.execute('select distinct ref,alt,chrom,chrSta from %s where %s="%s" and %s like "%%%s%%" and (samp_id="%s" or samp_id="%s")' % \
						(tbl, c_gene_sym,geneN, col,mutName, sId_p,sId_r))
					(ref,alt,chrom,loc) = cursor.fetchone()

					if not r_p:
						r_p = lookupPileup(pileupDirL,sId_p,chrom,loc,ref,alt)

					if not r_r:
						r_r = lookupPileup(pileupDirL,sId_r,chrom,loc,ref,alt)

			print sId_p,sId_r, mutType, geneN, mutName, r_p,r_r

			if r_p and r_r:
				if not (max(r_p[0],r_r[0])<=2 or max(r_p[1],r_r[1])<=2):
					resultL.append((geneN,mutType,mutName,sId_p,sId_r,r_p[0],r_p[1],r_r[0],r_r[1]))

	resultL_mut = filter(lambda x: x[1]=='MUT',resultL)
	resultL_oth = filter(lambda x: x[1]!='MUT',resultL)

	for r in resultL_mut:

		overlap = filter(lambda x: x[0]==r[0] and x[2:5]==r[2:5], resultL_oth)

		if overlap:
			resultL_oth.remove(overlap[0])

		resultL_oth.append(r)

	outFile = open(outFileName,'w')

	outFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % ('geneN','mutType','mutName','sId_p','sId_r','p_mut','p_ref','r_mut','r_ref'))

	for r in resultL_oth:
		outFile.write('\t'.join(map(str,r))+'\n')

	outFile.close()
	con.close()


#mutL_egfr = [('EGFR','SKIP','2-7,2-6'), ('EGFR','SKIP','25-27,24-26'), ('EGFR','MUT','A289')]
#mutL_idh1 = [('IDH1','MUT','R132'),('IDH1','MUTR','R132')]
#mutL_tp53 = [('TP53','MUT','T125'),('TP53','MUTR','T125'), ('TP53','MUT','R273'),('TP53','MUTR','R273'), ('TP53','MUT','R282'),('TP53','MUTR','R282'), ('TP53','MUT','R248'),('TP53','MUTR','R248'), ('TP53','MUT','R158'),('TP53','MUTR','R158'), ('TP53','MUT','A138'),('TP53','MUTR','A138'), ('TP53','MUT','Y127'),('TP53','MUTR','Y127'), ('TP53','MUT','R82'),('TP53','MUTR','R82')]
#mutL_other = [('BRAF','MUT','V600'),('BRAF','MUTR','V600'), ('APC','MUT','R876'),('APC','MUTR','R876'), ('PTEN','MUT','C136'),('PTEN','MUTR','C136'), ]
#mutL = mutL_egfr + mutL_tp53 + mutL_idh1 + mutL_other

mutL_idh1 = [('IDH1','MUT','R132')]
mutL_pten = [('PTEN','MUT','D24'),('PTEN','MUT','R173'),('PTEN','MUT','R130'),('PTEN','MUT','C136'),('PTEN','MUT','Q245'),('PTEN','MUT','P204'),('PTEN','MUT','V166')]
mutL_tp53 = [('TP53','MUT','E294'),('TP53','MUT','R282'),('TP53','MUT','Y220'),('TP53','MUT','Y163'),('TP53','MUT','R273'),('TP53','MUT','R248'),('TP53','MUT','Y234'),\
	('TP53','MUT','T155'),('TP53','MUT','G199'),('TP53','MUT','R175'),('TP53','MUT','H179'),('TP53','MUT','C242'),('TP53','MUT','F270'),('TP53','MUT','C176'),\
	('TP53','MUT','Y205'),('TP53','MUT','P190'),('TP53','MUT','A161'),('TP53','MUT','A138'),('TP53','MUT','T125'),('TP53','MUT','R158')]
mutL_egfr = [('EGFR','MUT','A289'),('EGFR','MUT','T263'),('EGFR','MUT','G598'),('EGFR','MUT','Y225'),('EGFR','MUT','A1148'), \
	('EGFR','SKIP','2-7,2-6'),('EGFR','SKIP','25-27,24-26'),('EGFR','SKIP','25-26,24-25')]
mutL_tmp = mutL_egfr
mutL = list(mutL_tmp)

for x in mutL_tmp:
	y = list(x)
	y[1] = 'MUTR'
	mutL.append(tuple(y))

main('/EQL1/PrimRecur/paired/df_paired_mut.txt')
