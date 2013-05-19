#!/usr/bin/python

import sys, cgi, re
import mymysql

dbN = 'ircr1' # 'tcga1'

(con,cursor) = mymysql.connectDB(db=dbN)

#cursor.execute('create temporary table t_m as select * from splice_fusion where nPos>=2')
cursor.execute('create temporary table t_m as select * from splice_fusion')
cursor.execute('alter table t_m add index (samp_id,loc1)')
cursor.execute('alter table t_m add index (samp_id,loc2)')

cursor.execute('drop table if exists splice_fusion_AF')

cursor.execute('create table splice_fusion_AF as \
	select t_m.samp_id,loc1,loc2,gene_sym1,gene_sym2,ftype,exon1,exon2,frame,nReads,nPos,nReads_w1,nReads_w2 from t_m \
	left join splice_normal_loc1 t_w1 using (samp_id,loc1) left join splice_normal_loc2 t_w2 using (samp_id,loc2)')
