#!/usr/bin/python

import sys, numpy
import mymysql


def main():

	con,cursor = mymysql.connectDB(db='tcga1')

	cursor.execute('create temporary table t_EGFR as \
		select platform,pId,geneName,loc,sum(fraction)/count(fraction) fraction from tcga1.methyl where TN="T" and geneName = "EGFR" \
		group by platform, pId, loc')

	cursor.execute('alter table t_EGFR add index (geneName)')
	cursor.execute('alter table t_EGFR add index (pId)')

	cursor.execute('SELECT distinct platform,loc FROM t_EGFR')
	results1 = cursor.fetchall()

	output = []

	for (plat,loc) in results1:

		#cursor.execute('select fraction,z_score from methyl_pId, array_gene_expr where platform="%s" and loc="%s" and gene_sym="MGMT" and pId=samp_id' % (plat,loc))
		cursor.execute('select fraction,log2(rpkm+1) from t_EGFR, rpkm_gene_expr where platform="%s" and loc="%s" and gene_sym="EGFR" and pId=samp_id' % (plat,loc))
		results2 = cursor.fetchall()

		methyl,expr = zip(*results2)

		r = numpy.corrcoef(methyl,expr)[0,1]

		output.append((plat,loc,len(methyl),r))

	output.sort(lambda x,y: cmp(y[-1],x[-1]))

	for (plat,loc,n,r) in output:
		print '%s\t%s\t%s\t%.3f' % (plat,loc,n,r)

main()
