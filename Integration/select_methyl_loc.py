#!/usr/bin/python

import sys, numpy
import mymysql


def main():

	con,cursor = mymysql.connectDB(db='tcga1')

	cursor.execute('SELECT distinct platform,loc FROM methyl_pId')
	results1 = cursor.fetchall()

	output = []

	for (plat,loc) in results1:

		#cursor.execute('select fraction,z_score from methyl_pId, array_gene_expr where platform="%s" and loc="%s" and gene_sym="MGMT" and pId=samp_id' % (plat,loc))
		cursor.execute('select fraction,log2(rpkm+1) from methyl_pId, rpkm_gene_expr where platform="%s" and loc="%s" and gene_sym="MGMT" and pId=samp_id' % (plat,loc))
		results2 = cursor.fetchall()

		methyl,expr = zip(*results2)

		r = numpy.corrcoef(methyl,expr)[0,1]

		output.append((plat,loc,len(methyl),r))

	output.sort(lambda x,y: cmp(y[-1],x[-1]))

	for (plat,loc,n,r) in output:
		print '%s\t%s\t%s\t%.2f' % (plat,loc,n,r)

main()
