#!/usr/bin/python

import sys, cgi, re
import mymysql

dbN = 'ircr1' # 'tcga1'

(con,cursor) = mymysql.connectDB(db=dbN)

cursor.execute('create temporary table t_m as select * from splice_eiJunc')
cursor.execute('alter table t_m add index (samp_id,loc)')

cursor.execute('drop table if exists splice_eiJunc_AF')

cursor.execute('create table splice_eiJunc_AF as \
	select t_m.samp_id,loc,gene_sym,juncInfo,juncAlias,t_m.nReads,t_w.nReads_w1 nReads_w \
	from t_m left join splice_normal_loc1 t_w on t_m.samp_id=t_w.samp_id and t_m.loc=t_w.loc1')

cursor.execute('alter table splice_eiJunc_AF add index (samp_id,loc)')
cursor.execute('alter table splice_eiJunc_AF add index (samp_id,gene_sym,juncAlias,nReads,nReads_w)')
