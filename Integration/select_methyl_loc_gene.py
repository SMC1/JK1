#!/usr/bin/python

import sys, numpy
import mymysql


def main():

	con,cursor = mymysql.connectDB(db='tcga1')

	cursor.execute('select distinct platform from methyl')
	platformL = cursor.fetchall()

	for (platform,) in platformL:

		cursor.execute('select distinct geneName from methyl where geneName <>"" and platform="%s"' % platform)
		results = cursor.fetchall()

		for (gN,) in results:

			cursor.execute('SELECT distinct loc FROM methyl where geneName ="%s" and platform="%s"' % (gN,platform))
			results1 = cursor.fetchall()

			output = []

			for (loc,) in results1:

				cursor.execute('create temporary table t_rpkm as select samp_id,log2(rpkm+1) as rpkm_log from rpkm_gene_expr where gene_sym="%s"' % gN)
				cursor.execute('create temporary table t_methyl as select * from methyl where geneName="%s" and platform="%s"' % (gN,platform))
				cursor.execute('select fraction,rpkm_log from t_methyl, t_rpkm where loc="%s" and pId=samp_id' % (loc))
				
				results2 = cursor.fetchall()
				
				cursor.execute('drop table t_rpkm,t_methyl')
				
				if len(results2) == 0:
					continue

				methyl,expr = zip(*results2)

				r = numpy.corrcoef(methyl,expr)[0,1]

				output.append((platform,loc,len(methyl),r))

			output.sort(lambda x,y: cmp(y[-1],x[-1]))
			
			try:
				(plat, loc, n, r) = output[-1]
			except:
				continue

			print '%s\t%s\t%s\t%s\t%.2f' % (plat,gN,loc,n,r)

main()
