#!/usr/bin/python

import sys
import mymysql

dTypeH = {'CNA':('array_cn','value_log2'), 'CNX':('xsq_cn','value_log2'), 'Expr':('array_gene_expr_ori','value'), 'RPKM':('rpkm_gene_expr','log2(rpkm+1)')}
dbH = {'tcga1':'TCGA-GBM', 'ircr1':'IRCR-GBM'}

def main(outFileName,dbName):

	(con,cursor) = mymysql.connectDB(db=dbName)

	cursor.execute('select distinct samp_id from sample_tag where substring(tag,1,6)="pair_R" and \
		samp_id!="S042" and samp_id not like "%_X" and substring(samp_id,length(samp_id)-1)!="_2" and \
		find_in_set(samp_id,"S437,S586,S023,S697,S372,S538,S458,S453,S428,S460,S768,S780,S640,S096,S671,S592,S572,S520,S1A,S2A,S3A,S4A,S5A,S6A,S7A,S8A,S9A,S10A,S11A,S12A,S13A,S14A,S722,S171,S121,S652,S752,S386")>=1')
	sIdL_prim = [x for (x,) in cursor.fetchall()]

	print sIdL_prim

	resultL = []

	for dType in dTypeL:

		for geneN in geneL:

			for sId_p in sIdL_prim:

				cursor.execute('select t1.samp_id from sample_tag t1 where t1.tag="pair_P:%s" and \
					"%s" in (select t2.samp_id from sample_tag t2 where t2.tag=concat("pair_R:",t1.samp_id))' % (sId_p,sId_p))
				(sId_r,) = cursor.fetchone()

#				if sId_p=='S520':
#					sId_r = 'S602'

				cursor.execute('select %s from %s where gene_sym="%s" and samp_id="%s"' % (dTypeH[dType][1],dTypeH[dType][0],geneN,sId_p))
				r_p = cursor.fetchone()

				cursor.execute('select %s from %s where gene_sym="%s" and samp_id="%s"' % (dTypeH[dType][1],dTypeH[dType][0],geneN,sId_r))
				r_r = cursor.fetchone()

				if r_p and r_r:
					resultL.append((dType,geneN,sId_p,sId_r,r_p[0],r_r[0]))
	
	resultL_cna = filter(lambda x: x[0]=='CNA',resultL)
	resultL_oth = filter(lambda x: x[0]!='CNA',resultL)

	for r in resultL_cna:

		overlap = filter(lambda x: x[0]=='CNX' and x[1:4]==r[1:4], resultL_oth)

		if overlap:
			resultL_oth.remove(overlap[0])

		resultL_oth.append(r)

	outFile = open(outFileName,'w')
	outFile.write('%s\t%s\t%s\t%s\t%s\t%s\n' % ('dType','geneN','sId_p','sId_r','val_p','val_r'))

	for r in resultL_oth:
		outFile.write('%s\t%s\t%s\t%s\t%.2f\t%.2f\n' % r)

	outFile.close()
	con.close()

geneL = ['EGFR','CDK4','CDK6','PDGFRA','MET','MDM2','MDM4'] + ['CDKN2A','CDKN2B','CDKN2C','PTEN','RB1','NF1','QKI'] + ['FGFR1','FGFR2','FGFR3','IGF1R','IDH1','IDH2','TP53']
#dTypeL = ['Expr','CNA','RPKM']
dTypeL = ['CNA','CNX','RPKM']

#main('/EQL1/Phillips/paired/df_sel2.txt')
#main('/EQL2/SGI_20131031/RNASeq/results/df_paired_gene.txt')
main('/EQL1/PrimRecur/paired/df_paired_gene.txt','ircr1')
