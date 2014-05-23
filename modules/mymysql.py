#!/usr/bin/python

import MySQLdb
from mysetting import mysqlH

schemaH = {}
schemaH['xsq_cn'] = '''
CREATE TABLE xsq_cn (
	samp_id varchar(63) NOT NULL,
	gene_sym varchar(31) NOT NULL,
	value_log2 double NOT NULL,
	primary key (samp_id,gene_sym),
	index (gene_sym)
)
'''

schemaH['xsq_purity'] = '''
CREATE TABLE xsq_purity (
	samp_id varchar(63) NOT NULL,
	normal_frac varchar(10) NOT NULL,
	tumor_frac varchar(10) NOT NULL,
	primary key (samp_id)
)
'''

schemaH['xsq_cn_corr'] = '''
CREATE TABLE xsq_cn_corr (
	samp_id varchar(63) NOT NULL,
	gene_sym varchar(31) NOT NULL,
	value_log2 double NOT NULL,
	primary key (samp_id,gene_sym),
	index (gene_sym)
)
'''

schemaH['xsq_clonality'] = '''
CREATE TABLE xsq_clonality (
	samp_id varchar(63) NOT NULL,
	chrom varchar(15) NOT NULL,
	chrSta int unsigned NOT NULL,
	chrEnd int unsigned NOT NULL,
	ref varchar(15) NOT NULL,
	alt varchar(15) NOT NULL,
	clonality varchar(10) NOT NULL,
	index (samp_id,chrom,chrSta,chrEnd),
	index (samp_id,chrom,chrSta,chrEnd,ref,alt)
)
'''

def connectDB(user='cancer', passwd='cancer', db='ircr1', host='localhost'):

	con = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)

	con.autocommit = True
	cursor = con.cursor()

	return (con,cursor)

def dictSelect(sql,cursor):

	cursor.execute(sql)
	results = cursor.fetchall()

	colNameT = zip(*cursor.description)[0]

	dictL = []

	for row in results:
		dictL.append(dict(zip(colNameT,row)))

	return dictL

def create_DB(dbN='', dbText='', server='smc1'):
	(con, cursor) = connectDB(user='root', passwd='123456', host=mysqlH[server]['host'])

	cursor.execute('CREATE DATABASE IF NOT EXISTS %s' % dbN)
	cursor.execute("GRANT ALL ON %s.* TO 'cancer'@'localhost'" % dbN)
	cursor.execute('USE %s' % dbN)

	cursor.execute('SHOW TABLES FROM ircr1')
	tableL = filter(lambda x: x not in ['census','cosmic','rpkm_gene_expr_lg2'] and 'bak' not in x, [x for (x,) in cursor.fetchall()])

	for table in tableL:
		cursor.execute('CREATE TABLE IF NOT EXISTS %s LIKE ircr1.%s' % (table, table))
	
	(con, cursor) = connectDB(user='cancer', passwd='cancer', db='common', host=mysqlH[server]['host'])
	cursor.execute("INSERT INTO ircr_db_info (db_name, db_text) VALUES ('%s','%s')" % (dbN, dbText))

def reset_table(tableN, dataFileN, user='cancer', passwd='cancer', db='ircr1', host='localhost'):
	(con, cursor) = connectDB(user=user, passwd=passwd, db=db, host=host)

	cursor.execute('DROP TABLE IF EXISTS %s' % tableN)
	cursor.execute(schemaH[tableN])
	cursor.execute('LOAD DATA LOCAL INFILE "%s" INTO TABLE %s' % (dataFileN, tableN))
