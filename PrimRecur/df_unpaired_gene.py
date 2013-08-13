#!/usr/bin/python

import sys
import mymysql

dTypeH = {'CNA':('array_cn','value_log2'), 'Expr':('array_gene_expr_ori','value'), 'RPKM':('rpkm_gene_expr','log2(rpkm+1)')}
dbH = {'tcga1':'TCGA-GBM', 'ircr1':'IRCR-GBM'}

def main(outFileName,dbNL,dTypeL,geneNL):

	outFile = open(outFileName,'w')

	outFile.write('%s\t%s\t%s\t%s\t%s\t%s\n' % ('dbT','dType','geneN','PR','sId','val'))

	for dbN in dbNL:

		(con,cursor) = mymysql.connectDB(db=dbN)

		if dbN == 'ircr1':
			cursor.execute('create temporary table t_recur select distinct samp_id from sample_tag where substring(tag,1,6)="pair_P"')
		elif dbN == 'tcga1':
			cursor.execute('create temporary table t_recur select distinct samp_id from sample_tag where tag="Recur"')

		for dType in dTypeL:

			for geneN in geneNL:

				for PR in ('P','R'):

					cursor.execute('select samp_id,%s from %s where gene_sym="%s" and samp_id %s in (select samp_id from t_recur)' % (dTypeH[dType][1],dTypeH[dType][0],geneN,'not' if PR=='P' else ''))
					results = cursor.fetchall()

					for (sId,val) in results:
						outFile.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (dbH[dbN],dType,geneN,PR,sId,val))

		con.close()

	outFile.close()


geneNL = ['EGFR','CDK4','CDK6','PDGFRA','MET','MDM2','MDM4']+['CDKN2A','CDKN2B','CDKN2C','PTEN','RB1','NF1','QKI']
main('/EQL1/PrimRecur/unpaired/df_unpaired2.txt',['tcga1','ircr1'],['CNA','Expr','RPKM'],geneNL)
