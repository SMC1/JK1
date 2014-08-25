#!/usr/bin/python

import sys, os
import mymysql,mysetting

dTypeH = {'CNA':('array_cn','value_log2'), 'Expr':('array_gene_expr_ori','value'), 'RPKM':('rpkm_gene_expr','log2(rpkm+1)'), 'Methyl':('methyl_EGFR','fraction')}
dbH = {'tcga1':'TCGA-GBM', 'ircr1':'IRCR-GBM'}

def main(outFileName,dbNL,dTypeL,outDirName,outFileN):

	for dbN in dbNL:

		(con,cursor) = mymysql.connectDB(db=dbN)

		if dbN == 'ircr1':
			cursor.execute('create temporary table t_recur select distinct samp_id from sample_tag where substring(tag,1,6)="pair_P"')
		elif dbN == 'tcga1':
			cursor.execute('create temporary table t_recur select distinct samp_id from sample_tag where tag="Recur"')

		cursor.execute('SELECT distinct loc,geneName FROM tcga1.methyl_pId where platform="Infinium27k"')
		results1 = cursor.fetchall()

		for dType in dTypeL:

			for (loc,geneN) in results1:

				outFile = open(outFileName,'w')

				outFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % ('dbT','dType','geneN','PR','sId','val','loc'))

				for PR in ('P','R'):

					cursor.execute('select pId,%s from %s where platform="Infinium27k" and loc="%s" and geneName="%s" and pId %s in (select samp_id from t_recur)' % (dTypeH[dType][1],dTypeH[dType][0],loc,geneN,'not' if PR=='P' else ''))
					results = cursor.fetchall()

					for (sId,val) in results:
						outFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (dbH[dbN],dType,geneN,PR,sId,val,loc))

				outFile.close()
				
				os.system('Rscript %s/PrimRecur/unpaired_gene_methyl_ks.r %s %s &>> %s/error_kstest.txt' % (mysetting.SRC_HOME,outDirName,outFileN,outDirName))
		
		con.close()

main('/EQL1/PrimRecur/unpaired/df_unpaired_methyl.txt',['tcga1'],['Methyl'],'/EQL1/PrimRecur/unpaired','/EQL1/PrimRecur/unpaired/unpaired_methyl_ks2.txt')
#main('/EQL1/PrimRecur/unpaired/df_unpaired2.txt',['tcga1','ircr1'],['CNA','Expr','RPKM'],geneNL)
