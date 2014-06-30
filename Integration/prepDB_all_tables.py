#!/usr/bin/python

import mymysql
from mysetting import mysqlH

def main(newDBN='', server='smc1'):
	(con, cursor) = mymysql.connectDB(user='root', passwd='123456', host=mysqlH[server]['host'])
	
	cursor.execute('CREATE DATABASE IF NOT EXISTS %s' % newDBN)
	cursor.execute("GRANT ALL ON %s.* TO 'cancer'@'localhost'" % newDBN)

	cursor.execute('USE %s' % newDBN)

	cursor.execute('show tables from ircr1')
	tableL = filter(lambda x: x not in ['census','cosmic','rpkm_gene_expr_lg2'] and 'bak' not in x, [x for (x,) in cursor.fetchall()])

	for table in tableL:
		cursor.execute('CREATE TABLE IF NOT EXISTS %s LIKE ircr1.%s' % (table, table))

if __name__ == '__main__':
#	main(newDBN='IRCR_GBM_352_SCS')
#	main(newDBN='IRCR_GBM_363_SCS')
#	main(newDBN='RC085_LC195_bulk')
#	main(newDBN='LC_195_SCS')
	main(newDBN='CancerSCAN')
