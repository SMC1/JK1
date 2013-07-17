#!/usr/bin/python

import sys, numpy
import mymysql


def main():

	con,cursor = mymysql.connectDB(db='tcga1')

	cursor.execute('select distinct geneName from methyl_pId where geneName <>""')
	results = cursor.fetchall()

	for (gN,) in results:

		cursor.execute('SELECT distinct platform,loc FROM methyl_pId where geneName ="%s"' % gN)
		results1 = cursor.fetchall()

		output = []

		for (plat,loc) in results1:

			#cursor.execute('select fraction,z_score from methyl_pId, array_gene_expr where platform="%s" and loc="%s" and gene_sym="MGMT" and pId=samp_id' % (plat,loc))
			#cursor.execute('select fraction,log2(rpkm+1) from methyl_pId, rpkm_gene_expr where platform="%s" and loc="%s" and gene_sym="%s" and pId=samp_id' % (plat,loc,gN))
			cursor.execute('create temporary table t_rpkm as select samp_id,log2(rpkm+1) as rpkm_log from rpkm_gene_expr where gene_sym="%s"' % gN)
			cursor.execute('create temporary table t_methyl as select * from tcga1.methyl_pId where geneName="%s"' % gN)
			cursor.execute('select fraction,rpkm_log from t_methyl, t_rpkm where platform="%s" and loc="%s" and pId=samp_id' % (plat,loc))
			
			results2 = cursor.fetchall()
			
			cursor.execute('drop table t_rpkm,t_methyl')
			
			if len(results2) == 0:
				continue

			methyl,expr = zip(*results2)

			r = numpy.corrcoef(methyl,expr)[0,1]

			output.append((plat,loc,len(methyl),r))

		output.sort(lambda x,y: cmp(y[-1],x[-1]))

		for (plat,loc,n,r) in output:
			print '%s\t%s\t%s\t%s\t%.2f' % (gN,plat,loc,n,r)

main()
