#!/usr/bin/python

import sys
import mymysql

dTypeH = {'CNA':('array_cn','value_log2'), 'Expr':('array_gene_expr','z_score'), 'RPKM':('rpkm_gene_expr','log2(rpkm+1)')}
dbH = {'tcga1':'TCGA-GBM', 'ircr1':'IRCR-GBM'}

def main(outDirName):

	(con,cursor) = mymysql.connectDB(db='ircr1')

	cursor.execute('select distinct samp_id from sample_tag where substring(tag,1,6)="pair_R" and samp_id!="S042" and samp_id!="S520"')
	sIdL_prim = [x for (x,) in cursor.fetchall()]

	for dType in dTypeL:

		print dType

		outFile = open('%s/paired_df_%s.txt' % (outDirName,dType),'w')
		outFile.write('%s\t%s\t%s\t%s\t%s\n' % ('sId_p','sId_r','geneN','val_p','val_r'))

		for sId_p in sIdL_prim:
			
			print '\t%s' % sId_p

			cursor.execute('select samp_id from sample_tag where tag="pair_P:%s"' % sId_p)
			(sId_r,) = cursor.fetchone()

			cursor.execute('drop table if exists tP')
			cursor.execute('drop table if exists tR')

			cursor.execute('create temporary table tP select gene_sym,%s vP from %s where samp_id="%s"' % (dTypeH[dType][1],dTypeH[dType][0],sId_p))
			cursor.execute('alter table tP add index (gene_sym)')

			cursor.execute('create temporary table tR select gene_sym,%s vR from %s where samp_id="%s"' % (dTypeH[dType][1],dTypeH[dType][0],sId_r))
			cursor.execute('alter table tR add index (gene_sym)')

			cursor.execute('select gene_sym,vP,vR from tP join tR using (gene_sym)')
			results = cursor.fetchall()

			for (geneN,vP,vR) in results:
				outFile.write('%s\t%s\t%s\t%.2f\t%.2f\n' % (sId_p,sId_r,geneN,vP,vR))

		outFile.close()

	con.close()

#dTypeL = ['Expr','CNA','RPKM']
dTypeL = ['CNA','RPKM']

main('/EQL1/PrimRecur/paired')
