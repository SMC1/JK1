#!/usr/bin/python

import sys, cgi, re
import mymysql

dbN = 'ircr1' #'tcga1' 

(con,cursor) = mymysql.connectDB(db=dbN)

cursor.execute('drop table if exists splice_normal_loc1')
cursor.execute('create table splice_normal_loc1 as select samp_id,loc1,sum(nReads) nReads_w1 from splice_normal group by samp_id,loc1')
cursor.execute('alter table splice_normal_loc1 add index (samp_id,loc1)')

cursor.execute('drop table if exists splice_normal_loc2')
cursor.execute('create table splice_normal_loc2 as select samp_id,loc2,sum(nReads) nReads_w2 from splice_normal group by samp_id,loc2')
cursor.execute('alter table splice_normal_loc2 add index (samp_id,loc2)')
