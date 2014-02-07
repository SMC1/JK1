#!/usr/bin/python

import sys, cgi, re
import mymysql

def main(dbN='ircr1', cursor=None):
	if cursor == None:
		(con,cursor) = mymysql.connectDB(db=dbN)

	#cursor.execute('create temporary table t_m as select * from splice_skip where nPos>=5')
	cursor.execute('create temporary table t_m as select * from splice_skip')
	cursor.execute('alter table t_m add index (samp_id,loc1)')
	cursor.execute('alter table t_m add index (samp_id,loc2)')

	cursor.execute('drop table if exists splice_skip_AF')

	cursor.execute('create table splice_skip_AF as \
		select t_m.samp_id,loc1,loc2,gene_sym,frame,delExons,exon1,exon2,nReads,nPos,nReads_w1,nReads_w2 from t_m \
		left join splice_normal_loc1 t_w1 using (samp_id,loc1) left join splice_normal_loc2 t_w2 using (samp_id,loc2)')

	cursor.execute('alter table splice_skip_AF add index (samp_id,gene_sym,delExons,nReads,nReads_w1)')
	cursor.execute('alter table splice_skip_AF add index (samp_id,loc1,loc2)')
	cursor.execute('alter table splice_skip_AF add index (samp_id,delExons)')

if __name__ == '__main__':
	main()
