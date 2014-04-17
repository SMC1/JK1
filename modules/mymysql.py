#!/usr/bin/python

import MySQLdb

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

def reset_table(tableN, dataFileN, user='cancer', passwd='cancer', db='ircr1', host='localhost'):
	(con, cursor) = connectDB(user=user, passwd=passwd, db=db, host=host)

	cursor.execute('DROP TABLE IF EXISTS %s' % tableN)
	cursor.execute(schemaH[tableN])
	cursor.execute('LOAD DATA LOCAL INFILE "%s" INTO TABLE %s' % (dataFileN, tableN))
