#!/usr/bin/python

import sys
import mymysql

dTypeH = {'CNA':('array_cn','value_log2'), 'Expr':('array_gene_expr_ori','value'), 'RPKM':('rpkm_gene_expr','log2(rpkm+1)')}
dbH = {'tcga1':'TCGA-GBM', 'ircr1':'IRCR-GBM'}

def main(outFileName):

	(con,cursor) = mymysql.connectDB(db='ircr1')

	outFile = open(outFileName,'w')

	cursor.execute('select distinct samp_id from sample_tag where substring(tag,1,6)="pair_R" and samp_id!="S520"')
	sIdL_prim = [x for (x,) in cursor.fetchall()]

	outFile.write('%s\t%s\t%s\t%s\t%s\t%s\n' % ('dType','geneN','sId_p','sId_r','val_p','val_r'))

	for dType in dTypeL:

		for geneN in geneL:

			for sId_p in sIdL_prim:

				cursor.execute('select samp_id from sample_tag where tag="pair_P:%s"' % sId_p)
				(sId_r,) = cursor.fetchone()

				cursor.execute('select %s from %s where gene_sym="%s" and samp_id="%s"' % (dTypeH[dType][1],dTypeH[dType][0],geneN,sId_p))
				r_p = cursor.fetchone()

				cursor.execute('select %s from %s where gene_sym="%s" and samp_id="%s"' % (dTypeH[dType][1],dTypeH[dType][0],geneN,sId_r))
				r_r = cursor.fetchone()

				if r_p and r_r:
					outFile.write('%s\t%s\t%s\t%s\t%.2f\t%.2f\n' % (dType,geneN,sId_p,sId_r,r_p[0],r_r[0]))

	outFile.close()
	con.close()

geneL = ['EGFR','CDK4','CDK6','PDGFRA','MET','MDM2','MDM4']+['CDKN2A','CDKN2B','CDKN2C','PTEN','RB1','NF1','QKI']
dTypeL = ['Expr','CNA','RPKM']

#main('/EQL1/Phillips/paired/df_sel2.txt')
main('/EQL1/PrimRecur/paired/df_paired_gene.txt')
