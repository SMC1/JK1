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

schemaH['cs_cn'] = '''
CREATE TABLE cs_cn (
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

schemaH['mutation_ctr'] = '''
CREATE TABLE mutation_ctr (
	chrom varchar(15) NOT NULL,
	chrSta int unsigned NOT NULL,
	chrEnd int unsigned NOT NULL,
	ref varchar(15) NOT NULL,
	alt varchar(15) NOT NULL,
	count int unsigned NOT NULL,
	index (chrom,chrSta,chrEnd,ref,alt)
)
'''

## additional column: strand_cnt
schemaH['mutation_cs'] = '''
CREATE TABLE mutation_cs (
	samp_id varchar(63) NOT NULL,
	chrom varchar(8) NOT NULL,
	chrSta int unsigned NOT NULL,
	chrEnd int unsigned NOT NULL,
	ref varchar(63) NOT NULL,
	alt varchar(63) NOT NULL,
	n_nReads_ref mediumint unsigned,
	n_nReads_alt mediumint unsigned,
	nReads_ref mediumint unsigned NOT NULL,
	nReads_alt mediumint unsigned NOT NULL,
	strand_cnt varchar(127),
	gene_sym varchar(31) NOT NULL,
	ch_dna varchar(63) NOT NULL,
	ch_aa varchar(63) NOT NULL,
	ch_type varchar(127) NOT NULL,
	cosmic text,
	tcga text,
	index (samp_id,gene_sym),
	index (samp_id,chrom,chrSta,chrEnd),
	index (samp_id,chrom,chrSta,ref,alt),
	index (samp_id,chrom,chrSta,chrEnd,ref,alt)
)
'''

schemaH['mutation'] = '''
CREATE TABLE mutation (
	samp_id varchar(63) NOT NULL,
	chrom varchar(8) NOT NULL,
	chrSta int unsigned NOT NULL,
	chrEnd int unsigned NOT NULL,
	ref varchar(63) NOT NULL,
	alt varchar(63) NOT NULL,
	nReads_ref mediumint unsigned NOT NULL,
	nReads_alt mediumint unsigned NOT NULL,
	strand char(1) NOT NULL,
	gene_symL varchar(64),
	ch_dna varchar(127),
	ch_aa varchar(63),
	ch_type varchar(127),
	cosmic text,
	mutsig text,
	index (samp_id,gene_symL),
	index (samp_id,chrom,chrSta,chrEnd),
	index (samp_id,chrom,chrSta,ref,alt),
	index (samp_id,chrom,chrSta,chrEnd,ref,alt)
)
'''

schemaH['mutation_normal_tmp'] = '''
CREATE TABLE mutation_normal_tmp (
	samp_id varchar(63) NOT NULL,
	chrom varchar(8) NOT NULL,
	chrSta int unsigned NOT NULL,
	chrEnd int unsigned NOT NULL,
	ref varchar(63) NOT NULL,
	alt varchar(63) NOT NULL,
	n_nReads_ref mediumint unsigned,
	n_nReads_alt mediumint unsigned,
	nReads_ref mediumint unsigned NOT NULL,
	nReads_alt mediumint unsigned NOT NULL,
	strand_cnt varchar(127),
	gene_sym varchar(31) NOT NULL,
	ch_dna varchar(63) NOT NULL,
	ch_aa varchar(63) NOT NULL,
	ch_type varchar(127) NOT NULL,
	cosmic text,
	tcga text,
	index (samp_id,gene_sym),
	index (samp_id,chrom,chrSta,chrEnd),
	index (samp_id,chrom,chrSta,ref,alt),
	index (samp_id,chrom,chrSta,chrEnd,ref,alt)
)
'''

schemaH['id_conversion'] = '''
CREATE TABLE id_conversion (
	old_id varchar(63) NOT NULL,
	new_id varchar(63) NOT NULL,
	index (old_id,new_id)
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

def copy_table_s(fromDB, toDB, tableN, samp_id, user='cancer', passwd='cancer', host='localhost'):
	print fromDB,toDB,tableN
	(con, cursor) = connectDB(user=user, passwd=passwd, db=fromDB, host=host)
	cursor.execute('''ALTER TABLE %s.%s DISABLE KEYS''' % (toDB, tableN))
	cursor.execute('''DELETE FROM %s.%s WHERE samp_id='%s' ''' % (toDB, tableN, samp_id))
	cursor.execute('''INSERT INTO %s.%s SELECT * FROM %s.%s WHERE samp_id='%s' ''' % (toDB,tableN, fromDB,tableN, samp_id))
	cursor.execute('''ALTER TABLE %s.%s ENABLE KEYS''' % (toDB, tableN))
	

def reset_table(tableN, dataFileN, user='cancer', passwd='cancer', db='ircr1', host='localhost'):
	(con, cursor) = connectDB(user=user, passwd=passwd, db=db, host=host)

	cursor.execute('DROP TABLE IF EXISTS %s' % tableN)
	cursor.execute(schemaH[tableN])
	cursor.execute('LOAD DATA LOCAL INFILE "%s" INTO TABLE %s' % (dataFileN, tableN))

def clear_db(sampL, tableL, dbN='ircr1', user='cancer', passwd='cancer', host='localhost'):
	(con, cursor) = connectDB(user=user, passwd=passwd, db=dbN, host=host)

	for table in tableL:
		for samp in sampL:
			cursor.execute('''DELETE FROM %s WHERE samp_id='%s' ''' % (table, samp))
