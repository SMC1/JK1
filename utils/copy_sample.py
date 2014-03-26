#!/usr/bin/python

import mymysql
from mysetting import mysqlH

def copy_sample(sidL, toDB, fromDB='ircr1', server='smc1'):
	(con, cursor) = mymysql.connectDB(user=mysqlH[server]['user'],passwd=mysqlH[server]['passwd'],db=fromDB,host=mysqlH[server]['host'])

	cursor.execute('SHOW TABLES')
	tableL = filter(lambda x: x not in ['census','cosmic','rpkm_gene_expr_lg2'] and 'bak' not in x, [x for (x,) in cursor.fetchall()])

	for sid in sidL:
		for table in tableL:
			cursor.execute('SELECT count(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = "%s" AND TABLE_NAME = "%s" AND COLUMN_NAME = "samp_id"' % (fromDB, table))
			res = cursor.fetchone()[0]
			if int(res) < 1:
				continue
			print sid, table
			cursor.execute("INSERT INTO %s.%s SELECT * FROM %s WHERE samp_id='%s'" % (toDB, table, table, sid))

if __name__ == '__main__':
	copy_sample(sidL=['IRCR_GBM_352_TR','IRCR_GBM_352_TL'], toDB='IRCR_GBM_352_SCS', fromDB='ircr1', server='smc1')
