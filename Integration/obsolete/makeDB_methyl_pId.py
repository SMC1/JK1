#!/usr/bin/python

import sys, numpy
import mymysql


def main():

	con,cursor = mymysql.connectDB(db='tcga1')

	cursor.execute('select distinct geneName from methyl where geneName <>""')
	results = cursor.fetchall()

	for (gN,) in results[:1]:

		cursor.execute('drop table if exists methyl_pId')
		cursor.execute('create table methyl_pId as \
			SELECT platform,pId,geneName,loc,sum(fraction)/count(fraction) fraction FROM tcga1.methyl where TN="T" and geneName="%s" group by platform,pId,loc;' % gN)

	for (gN,) in results[1:]:
		
		cursor.execute('create temporary table t_methyl as \
			SELECT platform,pId,geneName,loc,sum(fraction)/count(fraction) fraction FROM tcga1.methyl where TN="T" and geneName="%s" group by platform,pId,loc;' % gN)

		cursor.execute('insert into methyl_pId select * from t_methyl')

		cursor.execute('drop table t_methyl')

	cursor.execute('alter table methyl_pId add index (geneName)')
	cursor.execute('alter table methyl_pId add index (pId)')

main()
