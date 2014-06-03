#!/usr/bin/python

import sys
import mymysql

dTypeH = {'PATHR':('rpkm_pathway','pathway','activity'), 'PATHA':('array_pathway','pathway','activity')}
dbH = {'tcga1':'TCGA-GBM', 'ircr1':'IRCR-GBM'}

def main(outFileName):

	(con,cursor) = mymysql.connectDB(db='ircr1')

	outFile = open(outFileName,'w')

	cursor.execute('select distinct samp_id from sample_tag where substring(tag,1,6)="pair_R" and samp_id!="S520" and samp_id!="S042"')
	sIdL_prim = [x for (x,) in cursor.fetchall()]

	outFile.write('%s\t%s\t%s\t%s\t%s\t%s\n' % ('dType','geneN','sId_p','sId_r','val_p','val_r'))

	for dType in dTypeL:

		for geneN in geneL:

			for sId_p in sIdL_prim:

				(tbl,col_name,col_val) = dTypeH[dType]

				cursor.execute('select samp_id from sample_tag where tag="pair_P:%s"' % sId_p)
				(sId_r,) = cursor.fetchone()

				cursor.execute('select %s from %s where %s="%s" and samp_id="%s"' % (col_val,tbl,col_name,geneN,sId_p))
				r_p = cursor.fetchone()

				cursor.execute('select %s from %s where %s="%s" and samp_id="%s"' % (col_val,tbl,col_name,geneN,sId_r))
				r_r = cursor.fetchone()

				if r_p and r_r:
					outFile.write('%s\t%s\t%s\t%s\t%.2f\t%.2f\n' % (dType,geneN,sId_p,sId_r,r_p[0],r_r[0]))

	outFile.close()
	con.close()

geneL = ['TGFb','NFkB']
dTypeL = ['PATHR','PATHA']

main('/EQL1/PrimRecur/paired/df_paired_pathway.txt')
