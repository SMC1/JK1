#!/usr/bin/python

import sys, numpy
import mymysql


def main(locFileName):

	con,cursor = mymysql.connectDB(db='tcga1')
	
	locFile = open(locFileName)

	cursor.execute('drop table if exists methyl_gene')

	for line in locFile:
		
		(plat, gN, loc, n, r) = line[:-1].split('\t')

		if r != '-nan' and float(r) <= -0.25:

			cursor.execute('create temporary table t_methyl as \
				select * from methyl where geneName="%s" and platform="%s" and loc="%s"' % (gN,plat,loc))
			
			cursor.execute('alter table t_methyl add column r float, add column n smallint unsigned')
			cursor.execute('update t_methyl set n=%s, r=%s' % (int(n),float(r)))

			try:
				cursor.execute('create table methyl_gene as \
					select platform,pId,geneName,loc,sum(fraction)/count(fraction) fraction, n, r from t_methyl group by pId')
			except:
				cursor.execute('insert into methyl_gene \
					select platform,pId,geneName,loc,sum(fraction)/count(fraction) fraction, n, r from t_methyl group by pId')

			cursor.execute('drop table t_methyl')

	cursor.execute('alter table methyl_gene add index (geneName)')
	cursor.execute('alter table methyl_gene add index (pId)')

main('/EQL1/TCGA/GBM/methyl/methyl_loc_wg.txt')
