#!/usr/bin/python

import sys, cgi, re
import mymysql

from datetime import datetime

def skip(dbN='ircr1', cursor=None):
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
	
	cursor.execute('drop temporary table if exists t_m')

def skip_s(sid, dbN='ircr1', cursor=None):
	if cursor == None:
		(con,cursor) = mymysql.connectDB(db=dbN)
	
	cursor.execute('CREATE TEMPORARY TABLE t_m AS SELECT * FROM splice_skip WHERE samp_id="%s"' % sid)
	cursor.execute('ALTER TABLE t_m ADD INDEX (samp_id,loc1)')
	cursor.execute('ALTER TABLE t_m ADD INDEX (samp_id,loc2)')

	cursor.execute('CREATE TEMPORARY TABLE loc1 AS SELECT * FROM splice_normal_loc1 WHERE samp_id="%s"' % sid)
	cursor.execute('ALTER TABLE loc1 ADD INDEX (samp_id,loc1)')
	cursor.execute('CREATE TEMPORARY TABLE loc2 AS SELECT * FROM splice_normal_loc2 WHERE samp_id="%s"' % sid)
	cursor.execute('ALTER TABLE loc2 ADD INDEX (samp_id,loc2)')
	cursor.execute('CREATE TEMPORARY TABLE af_m AS \
		SELECT t_m.samp_id,loc1,loc2,gene_sym,frame,delExons,exon1,exon2,nReads,nPos,nReads_w1,nReads_w2 FROM t_m \
		LEFT JOIN loc1 t_w1 USING (samp_id,loc1) LEFT JOIN loc2 t_w2 USING (samp_id,loc2)')

	cursor.execute('ALTER TABLE splice_skip_AF DISABLE KEYS')
	cursor.execute('INSERT INTO splice_skip_AF SELECT * FROM af_m')
	cursor.execute('ALTER TABLE splice_skip_AF ENABLE KEYS')
	cursor.execute('DROP TEMPORARY TABLE IF EXISTS t_m,af_m,loc1,loc2')

def fusion(dbN='ircr1', cursor=None):
	if cursor == None:
		(con,cursor) = mymysql.connectDB(db=dbN)

	#cursor.execute('create temporary table t_m as select * from splice_fusion where nPos>=2')
	cursor.execute('create temporary table t_m as select * from splice_fusion')
	cursor.execute('alter table t_m add index (samp_id,loc1)')
	cursor.execute('alter table t_m add index (samp_id,loc2)')

	cursor.execute('drop table if exists splice_fusion_AF')

	cursor.execute('create table splice_fusion_AF as \
		select t_m.samp_id,loc1,loc2,gene_sym1,gene_sym2,ftype,exon1,exon2,frame,nReads,nPos,nReads_w1,nReads_w2 from t_m \
		left join splice_normal_loc1 t_w1 using (samp_id,loc1) left join splice_normal_loc2 t_w2 using (samp_id,loc2)')
	
	cursor.execute('drop temporary table if exists t_m')

def fusion_s(sid, dbN='ircr1', cursor=None):
	if cursor == None:
		(con,cursor) = mymysql.connectDB(db=dbN)

	cursor.execute('CREATE TEMPORARY TABLE t_m AS SELECT * FROM splice_fusion WHERE samp_id="%s"' % sid)
	cursor.execute('ALTER TABLE t_m ADD INDEX (samp_id,loc1)')
	cursor.execute('ALTER TABLE t_m ADD INDEX (samp_id,loc2)')

	cursor.execute('CREATE TEMPORARY TABLE loc1 AS SELECT * FROM splice_normal_loc1 WHERE samp_id="%s"' % sid)
	cursor.execute('ALTER TABLE loc1 ADD INDEX (samp_id,loc1)')
	cursor.execute('CREATE TEMPORARY TABLE loc2 AS SELECT * FROM splice_normal_loc2 WHERE samp_id="%s"' % sid)
	cursor.execute('ALTER TABLE loc2 ADD INDEX (samp_id,loc2)')
	cursor.execute('CREATE TEMPORARY TABLE af_m AS \
		SELECT t_m.samp_id,loc1,loc2,gene_sym1,gene_sym2,ftype,exon1,exon2,frame,nReads,nPos,nReads_w1,nReads_w2 FROM t_m \
		LEFT JOIN loc1 t_w1 USING (samp_id,loc1) LEFT JOIN loc2 t_w2 USING (samp_id,loc2)')
	
	cursor.execute('ALTER TABLE splice_fusion_AF DISABLE KEYS')
	cursor.execute('INSERT INTO splice_fusion_AF SELECT * FROM af_m')
	cursor.execute('ALTER TABLE splice_fusion_AF ENABLE KEYS')
	cursor.execute('DROP TEMPORARY TABLE IF EXISTS t_m,af_m,loc1,loc2')

def eiJunc(dbN='ircr1', cursor=None):
	if cursor == None:
		(con,cursor) = mymysql.connectDB(db=dbN)

	cursor.execute('create temporary table t_m as select * from splice_eiJunc')
	cursor.execute('alter table t_m add index (samp_id,loc)')

	cursor.execute('drop table if exists splice_eiJunc_AF')

	cursor.execute('create table splice_eiJunc_AF as \
		select t_m.samp_id,loc,gene_sym,juncInfo,juncAlias,isLastExon,t_m.nReads,t_w.nReads_w1 nReads_w \
		from t_m left join splice_normal_loc1 t_w on t_m.samp_id=t_w.samp_id and t_m.loc=t_w.loc1')

	cursor.execute('alter table splice_eiJunc_AF add index (samp_id,loc)')
	cursor.execute('alter table splice_eiJunc_AF add index (samp_id,gene_sym,juncAlias,nReads,nReads_w)')

	cursor.execute('drop temporary table if exists t_m')

def eiJunc_s(sid, dbN='ircr1', cursor=None):
	if cursor == None:
		(con,cursor) = mymysql.connectDB(db=dbN)
	
	cursor.execute('CREATE TEMPORARY TABLE t_m AS SELECT * FROM splice_eiJunc WHERE samp_id="%s"' % sid)
	cursor.execute('ALTER TABLE t_m ADD INDEX (samp_id,loc)')

	cursor.execute('CREATE TEMPORARY TABLE loc1 AS SELECT * FROM splice_normal_loc1 WHERE samp_id="%s"' % sid)
	cursor.execute('ALTER TABLE loc1 ADD INDEX (samp_id,loc1)')
	cursor.execute('CREATE TEMPORARY TABLE af_m AS \
		SELECT t_m.samp_id,loc,gene_sym,juncInfo,juncAlias,isLastExon,t_m.nReads,t_w.nReads_w1 nReads_w \
		FROM t_m LEFT JOIN loc1 t_w ON t_m.samp_id=t_w.samp_id AND t_m.loc=t_w.loc1')
	
	cursor.execute('ALTER TABLE splice_eiJunc_AF DISABLE KEYS')
	cursor.execute('INSERT INTO splice_eiJunc_AF SELECT * FROM af_m')
	cursor.execute('ALTER TABLE splice_eiJunc_AF ENABLE KEYS')
	cursor.execute('DROP TEMPORARY TABLE IF EXISTS t_m,af_m,loc1')
