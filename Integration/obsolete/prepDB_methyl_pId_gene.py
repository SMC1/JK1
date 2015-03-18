#!/usr/bin/python

import sys, numpy
import mymysql


def main():

	con,cursor = mymysql.connectDB(db='tcga1')

	cursor.execute('select distinct geneName from methyl_rpkm')
	results = cursor.fetchall()

	for (gN,) in results:

		cursor.execute('create temporary table t_methyl as \
			select geneName,platform,loc,r from methyl_rpkm where geneName="%s" and r < -0.3 order by platform,r' % gN)
		cursor.execute('select geneName,platform,loc,r from t_methyl group by platform')
		results1 = cursor.fetchall()

		for (gN, plat, loc, r) in results1:
			cursor.execute('select pId,geneName,fraction FROM methyl_pId where geneName="%s" and platform="%s" and loc="%s"' % (gN,plat,loc))
			results2 = cursor.fetchall()
			
			for (pId, gN, f) in results2:
				print '%s\t%s\t%s\t%s\t%s' % (pId,gN,f,plat,r)

main()
